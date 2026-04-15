import os
import json
import pg8000

def db_connect():
    return pg8000.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        port=int(os.environ.get("DB_PORT", 5432))
    )

def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "GET,OPTIONS"
        },
        "body": json.dumps(body)
    }

def round1(value):
    return round(float(value), 1)

def lambda_handler(event, context):
    method = event.get("httpMethod", "GET")

    if method == "OPTIONS":
        return response(200, {"ok": True})

    conn = None
    cur = None

    try:
        conn = db_connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT bmi_group, bmi_5_17_years
            FROM bmi_5_17
            WHERE bmi_group IN (
                'Persons_Underweight',
                'Persons_Normal',
                'Persons_Overweight',
                'Persons_Obese'
            )
        """)
        bmi_rows = cur.fetchall()

        bmi_map = {row[0]: float(row[1]) for row in bmi_rows}
        bmi_order = [
            ("Persons_Underweight", "Underweight", "underweight"),
            ("Persons_Normal", "Healthy range", "normal"),
            ("Persons_Overweight", "Overweight", "overweight"),
            ("Persons_Obese", "Obese", "obese")
        ]

        bmi_total = sum(bmi_map.values())
        body_segments = []

        for key, label, slug in bmi_order:
            raw_value = bmi_map.get(key, 0)
            pct = round1((raw_value / bmi_total) * 100) if bmi_total else 0
            body_segments.append({
                "key": slug,
                "label": label,
                "value": pct
            })

        healthy_pct = next(
            (item["value"] for item in body_segments if item["key"] == "normal"),
            0
        )


        cur.execute("""
            SELECT category, value_5_17
            FROM sleep_weekend_week
            WHERE category LIKE 'Weeknight%%'
               OR category LIKE 'Weekend night%%'
               OR category LIKE 'Per night%%'
        """)
        sleep_rows = cur.fetchall()

        sleep_map = {row[0]: float(row[1]) for row in sleep_rows}

        sleep_bands = [
            "Less than 6 hours",
            "6 to less than 7 hours",
            "7 to less than 8 hours",
            "8 to less than 9 hours",
            "9 to less than 10 hours",
            "10 hours or more"
        ]

        def build_sleep_series(prefix):
            result = []
            for band in sleep_bands:
                full_key = f"{prefix} {band}"
                result.append({
                    "label": band,
                    "value": round1(sleep_map.get(full_key, 0))
                })
            return result

        weeknight = build_sleep_series("Weeknight")
        weekend = build_sleep_series("Weekend night")
        overall = build_sleep_series("Per night")

        sleep_top = max(overall, key=lambda x: x["value"]) if overall else {"label": "", "value": 0}


        cur.execute("""
            SELECT TRIM(category), value_5_17
            FROM physical_inactivity
            WHERE TRIM(section_heading) = 'Average daily inactivity'
              AND TRIM(category) NOT IN ('Total persons', 'Average daily inactivity')
        """)
        inactivity_rows = cur.fetchall()

        inactivity_map = {row[0]: float(row[1]) for row in inactivity_rows}
        inactivity_order = [
            "Less than 9 hours",
            "9 to less than 10 hours",
            "10 to less than 11 hours",
            "11 to less than 12 hours",
            "12 to less than 13 hours",
            "13 to less than 14 hours",
            "14 hours or more"
        ]

        inactivity_bands = [
            {
                "label": band,
                "value": round1(inactivity_map.get(band, 0))
            }
            for band in inactivity_order
        ]

        inactivity_top = max(inactivity_bands, key=lambda x: x["value"]) if inactivity_bands else {"label": "", "value": 0}

        payload = {
            "bodyBalance": {
                "headlinePct": healthy_pct,
                "headlineText": "of children are in a healthy weight range.",
                "segments": body_segments
            },
            "sleep": {
                "headlineBand": sleep_top["label"],
                "headlinePct": sleep_top["value"],
                "headlineText": "is the most common sleep band overall.",
                "weeknight": weeknight,
                "weekend": weekend,
                "overall": overall
            },
            "activity": {
                "headlineBand": inactivity_top["label"],
                "headlinePct": inactivity_top["value"],
                "headlineText": "is the largest inactivity band.",
                "bands": inactivity_bands
            }
        }

        return response(200, payload)

    except Exception as e:
        return response(500, {"error": str(e)})

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()