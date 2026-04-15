import os
import json
import pg8000


def normalize_username(username: str) -> str:
    return username.strip().lower().replace(" ", "")


def get_conn():
    return pg8000.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ.get("DB_PORT", "5432")),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
    )


def parse_body(event):
    body = event.get("body")
    if not body:
        return {}

    if event.get("isBase64Encoded"):
        import base64
        body = base64.b64decode(body).decode("utf-8")

    if isinstance(body, str):
        return json.loads(body)

    return body


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
        payload = parse_body(event)

        raw_username = payload.get("username", "")
        if not raw_username or not raw_username.strip():
            return response(400, {"error": "username is required"})

        username = normalize_username(raw_username)

        parent_name = payload.get("parentName")
        child_name = payload.get("childName")
        age_range = payload.get("ageRange")
        routine_type = payload.get("routineType")
        habits = payload.get("habits", [])
        concerns = payload.get("concerns", [])
        struggle = payload.get("struggle")
        confidence = payload.get("confidence")
        support_style = payload.get("supportStyle")
        recommendations = payload.get("recommendations", [])
        daily_plan = payload.get("dailyPlan", {})
        progress_items = payload.get("progressItems", [])
        next_action = payload.get("nextAction")
        mission = payload.get("mission")
        streak_days = int(payload.get("streakDays", 0))

        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO parent_profiles (
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
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s::jsonb, %s::jsonb, %s, %s, %s,
                %s::jsonb, %s::jsonb, %s::jsonb,
                %s, %s, %s
            )
            """,
            (
                username,
                parent_name,
                child_name,
                age_range,
                routine_type,
                json.dumps(habits),
                json.dumps(concerns),
                struggle,
                confidence,
                support_style,
                json.dumps(recommendations),
                json.dumps(daily_plan),
                json.dumps(progress_items),
                next_action,
                mission,
                streak_days,
            ),
        )

        conn.commit()

        return response(201, {
            "success": True,
            "message": "Parent profile saved successfully",
            "username": username
        })

    except Exception as e:
        if conn:
            conn.rollback()

        error_text = str(e).lower()

        if "duplicate key" in error_text or "unique constraint" in error_text:
            return response(409, {"error": "username already taken"})

        return response(500, {"error": str(e)})

    finally:
        if conn:
            conn.close()