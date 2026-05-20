"""
Create Parent Profile Lambda Function

This AWS Lambda function saves a new HealthyKids parent profile into
PostgreSQL/RDS.

Main responsibilities:
- Handles POST and OPTIONS requests.
- Reads and parses the request body from API Gateway.
- Normalises the family code / username before saving.
- Validates that a username has been provided.
- Connects to PostgreSQL/RDS using pg8000.
- Saves parent, child, quiz, recommendation, and dashboard progress data.
- Stores list/object fields as JSONB in the parent_profiles table.
- Returns the saved username and dashboard progress fields.
- Returns a clear conflict response if the username is already taken.

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


def normalize_username(username: str) -> str:
    """
    Normalises the family code / username before saving.

    This keeps usernames consistent by removing spaces and converting the value
    to lowercase.
    """
    return username.strip().lower().replace(" ", "")


def get_conn():
    """
    Creates and returns a PostgreSQL/RDS database connection.

    The strip calls remove accidental spaces or quotes from Lambda environment
    variable values.
    """
    return pg8000.connect(
        host=os.environ["DB_HOST"].strip().strip('"').strip("'"),
        port=int(os.environ.get("DB_PORT", "5432")),
        user=os.environ["DB_USER"].strip().strip('"').strip("'"),
        password=os.environ["DB_PASSWORD"].strip().strip('"').strip("'"),
        database=os.environ["DB_NAME"].strip().strip('"').strip("'"),
    )


def parse_body(event):
    """
    Parses the API Gateway request body.

    Supports normal JSON string bodies and base64-encoded bodies.
    """
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
    """
    Builds a standard API Gateway response.

    Includes JSON and CORS headers so the HealthyKids frontend can call this
    Lambda from the browser.
    """
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "POST,OPTIONS",
        },
        "body": json.dumps(body_dict, default=str),
    }


def lambda_handler(event, context):
    """
    Main Lambda entry point.

    Validates the incoming profile payload, saves the new parent profile,
    commits the transaction, and returns the saved profile identifiers.
    """
    conn = None

    try:
        # Detect the HTTP method from the API Gateway HTTP API event.
        method = event.get("requestContext", {}).get("http", {}).get("method", "POST")

        # Return early for browser CORS preflight requests.
        if method == "OPTIONS":
            return response(200, {"ok": True})

        # Parse the incoming JSON request body.
        payload = parse_body(event)

        # Validate and normalise the username/family code.
        raw_username = payload.get("username", "")
        if not raw_username or not raw_username.strip():
            return response(400, {"error": "username is required"})

        username = normalize_username(raw_username)

        # Read parent and child profile fields from the request payload.
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
        progress_items = payload.get("progressItems", {})

        # Read generated plan and streak values.
        next_action = payload.get("nextAction")
        mission = payload.get("mission")
        streak_days = int(payload.get("streakDays", 0))

        # New dashboard progress fields
        roadmap_progress = payload.get("roadmapProgress", {})
        today_schedule = payload.get("todaySchedule", {})
        planner_overrides = payload.get("plannerOverrides", {})

        # Open database connection and cursor.
        conn = get_conn()
        cur = conn.cursor()

        # Insert the new profile and store list/object fields as JSONB.
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
                streak_days,
                roadmap_progress,
                today_schedule,
                planner_overrides
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s::jsonb, %s::jsonb, %s, %s, %s,
                %s::jsonb, %s::jsonb, %s::jsonb,
                %s, %s, %s,
                %s::jsonb, %s::jsonb, %s::jsonb
            )
            RETURNING username
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
                json.dumps(roadmap_progress),
                json.dumps(today_schedule),
                json.dumps(planner_overrides),
            ),
        )

        # Commit the insert and read the returned username.
        saved_row = cur.fetchone()
        conn.commit()

        # Return the saved profile confirmation to the frontend.
        return response(201, {
            "success": True,
            "message": "Parent profile saved successfully",
            "username": saved_row[0],
            "roadmapProgress": roadmap_progress,
            "todaySchedule": today_schedule,
            "plannerOverrides": planner_overrides,
        })

    except Exception as e:
        # Roll back the transaction if the insert fails.
        if conn:
            conn.rollback()

        error_text = str(e).lower()

        # Return a clear conflict response when the username already exists.
        if "duplicate key" in error_text or "unique constraint" in error_text:
            return response(409, {"error": "username already taken"})

        # Return a readable error response for all other failures.
        return response(500, {"error": str(e)})

    finally:
        # Always close the database connection after the request finishes.
        if conn:
            conn.close()