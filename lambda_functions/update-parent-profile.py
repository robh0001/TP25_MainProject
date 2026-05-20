"""
Update Parent Profile Lambda Function

This AWS Lambda function updates an existing HealthyKids parent profile in
PostgreSQL/RDS using the family code / username provided in the API path.

Main responsibilities:
- Handles PUT and OPTIONS requests.
- Reads the username from route path parameters.
- Parses the request body from API Gateway.
- Normalises the username before querying the database.
- Checks that the parent profile exists before updating.
- Updates only the fields provided in the request payload.
- Stores dashboard plan/progress fields as JSONB.
- Updates the updated_at timestamp.
- Returns the updated dashboard progress fields to the frontend.

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
    Normalises the family code / username before database lookup.

    This keeps profile updates consistent by removing spaces and converting
    the value to lowercase.
    """
    return username.strip().lower().replace(" ", "")


def get_conn():
    """
    Creates and returns a PostgreSQL/RDS database connection.

    The strip calls remove accidental quotes or spaces from Lambda environment
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
    Lambda through the browser.
    """
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "PUT,OPTIONS",
        },
        "body": json.dumps(body_dict, default=str),
    }


def lambda_handler(event, context):
    """
    Main Lambda entry point.

    Validates the username, checks that the profile exists, builds a dynamic
    update query from the provided fields, commits the update, and returns the
    updated progress values.
    """
    conn = None

    try:
        # Detect the HTTP method from the API Gateway HTTP API event.
        method = event.get("requestContext", {}).get("http", {}).get("method", "PUT")

        # Return early for browser CORS preflight requests.
        if method == "OPTIONS":
            return response(200, {"ok": True})

        # Read the username/family code from the route path parameters.
        path_params = event.get("pathParameters") or {}
        raw_username = path_params.get("username", "")

        # Stop early if the route does not include a username.
        if not raw_username.strip():
            return response(400, {"error": "username is required"})

        # Normalise the username and parse the incoming JSON request body.
        username = normalize_username(raw_username)
        payload = parse_body(event)

        # Read optional profile update fields from the request payload.
        daily_plan = payload.get("dailyPlan")
        progress_items = payload.get("progressItems")
        streak_days = payload.get("streakDays")
        next_action = payload.get("nextAction")
        mission = payload.get("mission")

        # New dashboard progress fields
        roadmap_progress = payload.get("roadmapProgress")
        today_schedule = payload.get("todaySchedule")
        planner_overrides = payload.get("plannerOverrides")

        # Open database connection and cursor.
        conn = get_conn()
        cur = conn.cursor()

        # Check that the requested parent profile exists before updating.
        cur.execute(
            "SELECT 1 FROM parent_profiles WHERE username = %s LIMIT 1",
            (username,)
        )

        if cur.fetchone() is None:
            return response(404, {"error": "profile not found"})

        # Build the UPDATE statement dynamically using only fields provided.
        updates = []
        values = []

        # Update daily plan JSON if provided.
        if daily_plan is not None:
            updates.append("daily_plan = %s::jsonb")
            values.append(json.dumps(daily_plan))

        # Update progress items JSON if provided.
        if progress_items is not None:
            updates.append("progress_items = %s::jsonb")
            values.append(json.dumps(progress_items))

        # Update roadmap progress JSON if provided.
        if roadmap_progress is not None:
            updates.append("roadmap_progress = %s::jsonb")
            values.append(json.dumps(roadmap_progress))

        # Update today's schedule JSON if provided.
        if today_schedule is not None:
            updates.append("today_schedule = %s::jsonb")
            values.append(json.dumps(today_schedule))

        # Update planner overrides JSON if provided.
        if planner_overrides is not None:
            updates.append("planner_overrides = %s::jsonb")
            values.append(json.dumps(planner_overrides))

        # Update streak count if provided.
        if streak_days is not None:
            updates.append("streak_days = %s")
            values.append(int(streak_days))

        # Update next action text if provided.
        if next_action is not None:
            updates.append("next_action = %s")
            values.append(next_action)

        # Update mission text if provided.
        if mission is not None:
            updates.append("mission = %s")
            values.append(mission)

        # Always refresh the updated_at timestamp when a real update occurs.
        updates.append("updated_at = NOW()")

        # If only updated_at was added, no actual update fields were provided.
        if len(updates) == 1:
            return response(400, {"error": "no fields provided to update"})

        # Build the final update query and return key progress fields.
        query = f"""
            UPDATE parent_profiles
            SET {", ".join(updates)}
            WHERE username = %s
            RETURNING
                username,
                roadmap_progress,
                today_schedule,
                planner_overrides
        """

        # Add username as the final query parameter for the WHERE clause.
        values.append(username)

        # Execute and commit the profile update.
        cur.execute(query, tuple(values))
        updated_row = cur.fetchone()
        conn.commit()

        # Return confirmation and updated dashboard progress data.
        return response(200, {
            "success": True,
            "message": "Parent profile updated successfully",
            "username": updated_row[0],
            "roadmapProgress": updated_row[1] or {},
            "todaySchedule": updated_row[2] or {},
            "plannerOverrides": updated_row[3] or {},
        })

    except Exception as e:
        # Roll back the transaction if the update fails.
        if conn:
            conn.rollback()

        # Return a readable error response for debugging.
        return response(500, {"error": str(e)})

    finally:
        # Always close the database connection after the request finishes.
        if conn:
            conn.close()