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

def lambda_handler(event, context):
    try:
        query_params = event.get("queryStringParameters") or {}
        raw_username = query_params.get("username", "")

        if not raw_username.strip():
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "username is required"})
            }

        username = normalize_username(raw_username)

        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM parent_profiles WHERE username = %s LIMIT 1",
            (username,)
        )
        exists = cur.fetchone() is not None
        conn.close()

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