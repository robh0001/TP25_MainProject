import json
import os
import pg8000.native

DB_HOST = os.environ["DB_HOST"]
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_PORT = int(os.environ.get("DB_PORT", "5432"))

def response(status_code, body):
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
    method = event.get("requestContext", {}).get("http", {}).get("method", "GET")

    if method == "OPTIONS":
        return response(200, {})

    connection = None

    try:
        connection = pg8000.native.Connection(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
            timeout=8,
            ssl_context=True,
        )

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

        columns = [
            "id",
            "name",
            "area",
            "category",
            "ingredients",
            "steps",
        ]

        recipes = [dict(zip(columns, row)) for row in rows]

        return response(200, {
            "count": len(recipes),
            "recipes": recipes,
        })

    except Exception as error:
        print("ERROR:", str(error))

        return response(500, {
            "error": "Failed to load recipes",
            "details": str(error),
        })

    finally:
        if connection:
            connection.close()