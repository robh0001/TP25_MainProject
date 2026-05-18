"""
Get Parent Profile Lambda Function

This AWS Lambda function loads a saved parent profile from PostgreSQL/RDS
using the family code / username provided in the API path.

Main responsibilities:
- Reads the username from the route path parameters.
- Normalises the username before querying the database.
- Handles GET and OPTIONS requests.
- Adds CORS headers for frontend API access.
- Connects to PostgreSQL/RDS using pg8000.
- Loads the saved parent profile from the parent_profiles table.
- Converts database fields into frontend-friendly camelCase keys.
- Returns a clear error if the profile is missing or the database request fails.

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

    This keeps profile lookup consistent by removing spaces and converting
    the value to lowercase.
    """
    return username.strip().lower().replace(" ", "")


def get_conn():
    """
    Creates and returns a PostgreSQL/RDS database connection.

    The extra strip calls help remove accidental quotes or spaces from Lambda
    environment variable values.
    """
    return pg8000.connect(
        host=os.environ["DB_HOST"].strip().strip('"').strip("'"),
        port=int(os.environ.get("DB_PORT", "5432")),
        user=os.environ["DB_USER"].strip().strip('"').strip("'"),
        password=os.environ["DB_PASSWORD"].strip().strip('"').strip("'"),
        database=os.environ["DB_NAME"].strip().strip('"').strip("'"),
    )


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
            "Access-Control-Allow-Methods": "GET,OPTIONS",
        },
        "body": json.dumps(body_dict, default=str),
    }


def lambda_handler(event, context):
    """
    Main Lambda entry point.

    Handles CORS preflight requests, validates the username path parameter,
    loads the matching parent profile, and returns it in the format expected
    by the frontend.
    """
    conn = None

    try:
        # Detect the HTTP method from the API Gateway HTTP API event.
        method = event.get("requestContext", {}).get("http", {}).get("method", "GET")

        # Return early for browser CORS preflight requests.
        if method == "OPTIONS":
            return response(200, {"ok": True})

        # Read the username/family code from the route path parameters.
        path_params = event.get("pathParameters") or {}
        raw_username = path_params.get("username", "")

        # Stop early if the route does not include a username.
        if not raw_username.strip():
            return response(400, {"error": "username is required"})

        # Normalise the username before checking the database.
        username = normalize_username(raw_username)

        # Open a database connection and cursor.
        conn = get_conn()
        cur = conn.cursor()

        # Load the saved parent profile for the requested username.
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
                streak_days,
                roadmap_progress,
                today_schedule,
                planner_overrides
            FROM parent_profiles
            WHERE username = %s
            LIMIT 1
            """,
            (username,)
        )

        row = cur.fetchone()

        # Return a clear 404 response when no matching profile exists.
        if not row:
            return response(404, {"error": "profile not found"})

        # Convert the database row into the camelCase shape used by the frontend.
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
            "progressItems": row[12] or {},

            "nextAction": row[13],
            "mission": row[14],
            "streakDays": row[15] or 0,
            "roadmapProgress": row[16] or {},
            "todaySchedule": row[17] or {},
            "plannerOverrides": row[18] or {},
        }

        # Return the saved profile to the frontend.
        return response(200, profile)

    except Exception as e:
        # Return a readable error response if profile loading fails.
        return response(500, {"error": str(e)})

    finally:
        # Always close the database connection after the request finishes.
        if conn:
            conn.close()