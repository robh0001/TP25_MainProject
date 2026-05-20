"""
Recipes API Lambda Function

This AWS Lambda function loads recipe records from a PostgreSQL/RDS database
and returns them as JSON for the HealthyKids app.

Main responsibilities:
- Reads database connection settings from environment variables.
- Handles CORS responses for browser requests.
- Supports GET and OPTIONS requests.
- Connects to PostgreSQL/RDS using pg8000.
- Loads recipe data from the recipes table.
- Filters out rows containing non-ASCII text.
- Returns recipe count and recipe records as JSON.
- Returns a clear error response if the database query fails.

Required environment variables:
- DB_HOST
- DB_NAME
- DB_USER
- DB_PASSWORD

Optional environment variable:
- DB_PORT
"""

import json
import os
import pg8000.native


# Database connection settings from Lambda environment variables.
DB_HOST = os.environ["DB_HOST"]
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_PORT = int(os.environ.get("DB_PORT", "5432"))


def response(status_code, body):
    """
    Builds a standard API Gateway response.

    Includes CORS headers so the frontend can call this Lambda through
    API Gateway from the browser.
    """
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
            "Content-Type": "application/json",
        },
        "body": json.dumps(body, default=str),
    }


def lambda_handler(event, context):
    """
    Main Lambda entry point.

    Handles preflight OPTIONS requests, connects to the database, loads recipes,
    formats the result as JSON, and closes the database connection afterward.
    """
    # Detect the HTTP method from the API Gateway event.
    method = event.get("requestContext", {}).get("http", {}).get("method", "GET")

    # Return early for browser CORS preflight requests.
    if method == "OPTIONS":
        return response(200, {})

    connection = None

    try:
        # Open a PostgreSQL/RDS connection using pg8000.
        connection = pg8000.native.Connection(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
            timeout=8,
            ssl_context=True,
        )

        # Load recipe rows and exclude rows containing non-ASCII characters.
        rows = connection.run(r"""
            SELECT
                id,
                recipe_name AS name,
                cuisine_area AS area,
                category,
                ingredients,
                steps
            FROM recipes
            WHERE recipe_name !~ '[^\x00-\x7F]'
              AND cuisine_area !~ '[^\x00-\x7F]'
              AND category !~ '[^\x00-\x7F]'
              AND ingredients !~ '[^\x00-\x7F]'
              AND steps !~ '[^\x00-\x7F]'
            ORDER BY cuisine_area, recipe_name;
        """)

        # Column names used to convert each row tuple into a dictionary.
        columns = [
            "id",
            "name",
            "area",
            "category",
            "ingredients",
            "steps",
        ]

        # Convert database rows into JSON-friendly recipe objects.
        recipes = [dict(zip(columns, row)) for row in rows]

        # Return the recipes and total count to the frontend.
        return response(200, {
            "count": len(recipes),
            "recipes": recipes,
        })

    except Exception as error:
        # Log the detailed error in CloudWatch and return a readable API response.
        print("ERROR:", str(error))

        return response(500, {
            "error": "Failed to load recipes",
            "details": str(error),
        })

    finally:
        # Always close the database connection after the request finishes.
        if connection:
            connection.close()