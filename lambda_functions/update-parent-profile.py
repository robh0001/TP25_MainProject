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
        path_params = event.get("pathParameters") or {}
        raw_username = path_params.get("username", "")

        if not raw_username.strip():
            return response(400, {"error": "username is required"})

        username = normalize_username(raw_username)
        payload = parse_body(event)

        daily_plan = payload.get("dailyPlan")
        progress_items = payload.get("progressItems")
        streak_days = payload.get("streakDays")
        next_action = payload.get("nextAction")
        mission = payload.get("mission")

        conn = get_conn()
        cur = conn.cursor()

        # First check profile exists
        cur.execute(
            "SELECT 1 FROM parent_profiles WHERE username = %s LIMIT 1",
            (username,)
        )
        if cur.fetchone() is None:
            return response(404, {"error": "profile not found"})

        # Build dynamic update query
        updates = []
        values = []

        if daily_plan is not None:
            updates.append("daily_plan = %s::jsonb")
            values.append(json.dumps(daily_plan))

        if progress_items is not None:
            updates.append("progress_items = %s::jsonb")
            values.append(json.dumps(progress_items))

        if streak_days is not None:
            updates.append("streak_days = %s")
            values.append(int(streak_days))

        if next_action is not None:
            updates.append("next_action = %s")
            values.append(next_action)

        if mission is not None:
            updates.append("mission = %s")
            values.append(mission)

        updates.append("updated_at = NOW()")

        if len(updates) == 1:
            return response(400, {"error": "no fields provided to update"})

        query = f"""
            UPDATE parent_profiles
            SET {", ".join(updates)}
            WHERE username = %s
            RETURNING username
        """
        values.append(username)

        cur.execute(query, tuple(values))
        updated_row = cur.fetchone()
        conn.commit()

        return response(200, {
            "success": True,
            "message": "Parent profile updated successfully",
            "username": updated_row[0]
        })

    except Exception as e:
        if conn:
            conn.rollback()
        return response(500, {"error": str(e)})

    finally:
        if conn:
            conn.close()