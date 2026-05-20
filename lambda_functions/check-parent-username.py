"""
Check Username Availability Lambda Function

This AWS Lambda function checks whether a parent family code / username
already exists in the parent_profiles table.

Main responsibilities:
- Reads the username from query string parameters.
- Normalises the username before checking the database.
- Connects to PostgreSQL/RDS using pg8000.
- Checks whether the username already exists.
- Returns whether the username is available.
- Returns clear error responses for missing username or server errors.

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

    This keeps username checks consistent by removing spaces and converting
    the value to lowercase.
    """
    return username.strip().lower().replace(" ", "")


def get_conn():
    """
    Creates and returns a PostgreSQL/RDS database connection.

    Database settings are loaded from Lambda environment variables.
    """
    return pg8000.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ.get("DB_PORT", "5432")),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
    )


def lambda_handler(event, context):
    """
    Main Lambda entry point.

    Validates the username query parameter, checks whether it exists in the
    parent_profiles table, and returns an availability response.
    """
    try:
        # Read query string values from the API Gateway event.
        query_params = event.get("queryStringParameters") or {}
        raw_username = query_params.get("username", "")

        # Stop early if the username was not provided.
        if not raw_username.strip():
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "username is required"})
            }

        # Normalise the username so checks are case-insensitive and space-safe.
        username = normalize_username(raw_username)

        # Open the database connection and check whether the username exists.
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM parent_profiles WHERE username = %s LIMIT 1",
            (username,)
        )
        exists = cur.fetchone() is not None
        conn.close()

        # Return true when the username does not already exist.
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "available": not exists
            })
        }

    except Exception as e:
        # Return a readable error response if the database check fails.
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "error": str(e)
            })
        }