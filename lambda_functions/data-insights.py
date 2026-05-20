"""
Parent Data Insights Lambda Function

This AWS Lambda function loads child health insight data from PostgreSQL/RDS
and returns it as JSON for the HealthyKids statistics or insights page.

Main responsibilities:
- Connects to PostgreSQL/RDS using pg8000.
- Handles GET and OPTIONS requests.
- Adds CORS headers for frontend API access.
- Loads BMI, sleep, and physical inactivity data.
- Converts raw database values into frontend-friendly percentages.
- Builds chart-ready response sections for body balance, sleep, and activity.
- Returns a clear error response if the database query fails.

Required environment variables:
- DB_HOST
- DB_USER
- DB_PASSWORD
- DB_NAME

Optional environment variable:
- DB_PORT
"""

import os
import json
import pg8000


def db_connect():
    """
    Creates and returns a PostgreSQL/RDS database connection.

    Database credentials are read from Lambda environment variables.
    """
    return pg8000.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        port=int(os.environ.get("DB_PORT", 5432))
    )


def response(status_code, body):
    """
    Builds a standard API Gateway response.

    Includes JSON and CORS headers so the frontend can call this Lambda
    from the browser.
    """
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
    """
    Converts a value to float and rounds it to one decimal place.

    This keeps chart percentages consistent in the frontend.
    """
    return round(float(value), 1)


def lambda_handler(event, context):
    """
    Main Lambda entry point.

    Loads BMI, sleep, and physical inactivity data from the database,
    formats the data into chart-ready JSON, and returns it to the frontend.
    """
    # Detect the HTTP method from the API Gateway event.
    method = event.get("httpMethod", "GET")

    # Return early for browser CORS preflight requests.
    if method == "OPTIONS":
        return response(200, {"ok": True})

    conn = None
    cur = None

    try:
        # Open database connection and cursor.
        conn = db_connect()
        cur = conn.cursor()

        # Load BMI categories for children aged 5 to 17.
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

        # Convert BMI rows into a lookup map for easier percentage calculations.
        bmi_map = {row[0]: float(row[1]) for row in bmi_rows}

        # Defines the display order and frontend keys for BMI segments.
        bmi_order = [
            ("Persons_Underweight", "Underweight", "underweight"),
            ("Persons_Normal", "Healthy range", "normal"),
            ("Persons_Overweight", "Overweight", "overweight"),
            ("Persons_Obese", "Obese", "obese")
        ]

        # Calculate each BMI segment as a percentage of the total.
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

        # Find the healthy range percentage for the headline card.
        healthy_pct = next(
            (item["value"] for item in body_segments if item["key"] == "normal"),
            0
        )

        # Load sleep distribution data for weeknight, weekend, and overall sleep.
        cur.execute("""
            SELECT category, value_5_17
            FROM sleep_weekend_week
            WHERE category LIKE 'Weeknight%%'
               OR category LIKE 'Weekend night%%'
               OR category LIKE 'Per night%%'
        """)
        sleep_rows = cur.fetchall()

        # Convert sleep rows into a lookup map by category name.
        sleep_map = {row[0]: float(row[1]) for row in sleep_rows}

        # Sleep bands shown in the frontend charts.
        sleep_bands = [
            "Less than 6 hours",
            "6 to less than 7 hours",
            "7 to less than 8 hours",
            "8 to less than 9 hours",
            "9 to less than 10 hours",
            "10 hours or more"
        ]

        def build_sleep_series(prefix):
            """
            Builds a chart-ready sleep series for the selected sleep prefix.

            The prefix is used to separate Weeknight, Weekend night, and
            Per night data.
            """
            result = []
            for band in sleep_bands:
                full_key = f"{prefix} {band}"
                result.append({
                    "label": band,
                    "value": round1(sleep_map.get(full_key, 0))
                })
            return result

        # Build separate sleep series for frontend comparison charts.
        weeknight = build_sleep_series("Weeknight")
        weekend = build_sleep_series("Weekend night")
        overall = build_sleep_series("Per night")

        # Find the most common overall sleep band for the headline card.
        sleep_top = max(overall, key=lambda x: x["value"]) if overall else {"label": "", "value": 0}

        # Load average daily physical inactivity data.
        cur.execute("""
            SELECT TRIM(category), value_5_17
            FROM physical_inactivity
            WHERE TRIM(section_heading) = 'Average daily inactivity'
              AND TRIM(category) NOT IN ('Total persons', 'Average daily inactivity')
        """)
        inactivity_rows = cur.fetchall()

        # Convert inactivity rows into a lookup map by band.
        inactivity_map = {row[0]: float(row[1]) for row in inactivity_rows}

        # Inactivity bands shown in the frontend charts.
        inactivity_order = [
            "Less than 9 hours",
            "9 to less than 10 hours",
            "10 to less than 11 hours",
            "11 to less than 12 hours",
            "12 to less than 13 hours",
            "13 to less than 14 hours",
            "14 hours or more"
        ]

        # Build chart-ready inactivity band data.
        inactivity_bands = [
            {
                "label": band,
                "value": round1(inactivity_map.get(band, 0))
            }
            for band in inactivity_order
        ]

        # Find the largest inactivity band for the headline card.
        inactivity_top = max(inactivity_bands, key=lambda x: x["value"]) if inactivity_bands else {"label": "", "value": 0}

        # Final response structure consumed by the HealthyKids frontend.
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

        # Return the formatted insights payload to the frontend.
        return response(200, payload)

    except Exception as e:
        # Return a readable error response if any database query fails.
        return response(500, {"error": str(e)})

    finally:
        # Always close database resources after the request finishes.
        if cur:
            cur.close()
        if conn:
            conn.close()