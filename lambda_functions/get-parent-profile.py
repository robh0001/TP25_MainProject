import os
import json
import pg8000


def normalize_username(username: str) -> str:
    return username.strip().lower().replace(" ", "")


def get_conn():
    return pg8000.connect(
        host=os.environ["DB_HOST"].strip().strip('"').strip("'"),
        port=int(os.environ.get("DB_PORT", "5432")),
        user=os.environ["DB_USER"].strip().strip('"').strip("'"),
        password=os.environ["DB_PASSWORD"].strip().strip('"').strip("'"),
        database=os.environ["DB_NAME"].strip().strip('"').strip("'"),
    )


def response(status_code, body_dict):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "http://localhost:5173"
        },
        "body": json.dumps(body_dict)
    }


def lambda_handler(event, context):
    conn = None

    try:
        path_params = event.get("pathParameters") or {}
        raw_username = path_params.get("username", "")

        if not raw_username.strip():
            return response(400, {"error": "username is required"})

        username = normalize_username(raw_username)

        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
                username,
                parent_name,
                child_name,
                age_range,
                routine_type,
                habits,
                concerns,
                struggle,
                confidence,
                support_style,
                recommendations,
                daily_plan,
                progress_items,
                next_action,
                mission,
                streak_days
            FROM parent_profiles
            WHERE username = %s
            LIMIT 1
            """,
            (username,)
        )

        row = cur.fetchone()

        if not row:
            return response(404, {"error": "profile not found"})

        profile = {
            "username": row[0],
            "parentName": row[1],
            "childName": row[2],
            "ageRange": row[3],
            "routineType": row[4],
            "habits": row[5] or [],
            "concerns": row[6] or [],
            "struggle": row[7],
            "confidence": row[8],
            "supportStyle": row[9],
            "recommendations": row[10] or [],
            "dailyPlan": row[11] or {},
            "progressItems": row[12] or [],
            "nextAction": row[13],
            "mission": row[14],
            "streakDays": row[15] or 0,
        }

        return response(200, profile)

    except Exception as e:
        return response(500, {"error": str(e)})

    finally:
        if conn:
            conn.close()