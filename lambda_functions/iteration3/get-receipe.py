import os
import csv
import sys
import psycopg2
from psycopg2.extras import execute_values


CSV_FILE = os.getenv("CSV_FILE", "Multi_Cuisine_Recipe_Dataset.numbers")
TABLE_NAME = "recipes"


CREATE_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    id SERIAL PRIMARY KEY,
    recipe_name VARCHAR(150) NOT NULL,
    cuisine_area VARCHAR(50) NOT NULL,
    category VARCHAR(80) NOT NULL,
    ingredients TEXT NOT NULL,
    steps TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
"""

# Optional but useful for filtering recipes in the app.
CREATE_INDEXES_SQL = [
    f"CREATE INDEX IF NOT EXISTS idx_{TABLE_NAME}_cuisine_area ON {TABLE_NAME}(cuisine_area);",
    f"CREATE INDEX IF NOT EXISTS idx_{TABLE_NAME}_category ON {TABLE_NAME}(category);",
    f"CREATE INDEX IF NOT EXISTS idx_{TABLE_NAME}_recipe_name ON {TABLE_NAME}(recipe_name);",
]

INSERT_SQL = f"""
INSERT INTO {TABLE_NAME}
(recipe_name, cuisine_area, category, ingredients, steps)
VALUES %s;
"""


def validate_config():
    missing = []
    for key, value in {
        "DB_HOST": DB_HOST,
        "DB_NAME": DB_NAME,
        "DB_USER": DB_USER,
        "DB_PASS": DB_PASS,
    }.items():
        if not value or value.startswith("YOUR_"):
            missing.append(key)

    if missing:
        print("Missing database configuration:", ", ".join(missing))
        print("Set the values as environment variables or replace the placeholders in this file.")
        sys.exit(1)


def read_recipe_csv(csv_file):
    if not os.path.exists(csv_file):
        print(f"CSV file not found: {csv_file}")
        print("Place Multi_Cuisine_Recipe_Dataset.csv in the same folder as this script,")
        print("or set CSV_FILE=/path/to/Multi_Cuisine_Recipe_Dataset.csv")
        sys.exit(1)

    rows = []

    with open(csv_file, mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        expected_columns = {"name", "area", "category", "ingredients", "steps"}
        actual_columns = set(reader.fieldnames or [])

        if not expected_columns.issubset(actual_columns):
            print("CSV columns do not match the expected format.")
            print("Expected:", sorted(expected_columns))
            print("Found:", sorted(actual_columns))
            sys.exit(1)

        for row in reader:
            rows.append((
                row["name"].strip(),
                row["area"].strip(),
                row["category"].strip(),
                row["ingredients"].strip(),
                row["steps"].strip(),
            ))

    return rows


def main():
    validate_config()
    recipe_rows = read_recipe_csv(CSV_FILE)

    if not recipe_rows:
        print("No recipe rows found in the CSV.")
        return

    connection = None
    cursor = None

    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT,
            connect_timeout=10,
            sslmode="require"
        )

        print("Connected successfully to PostgreSQL/RDS")

        cursor = connection.cursor()

        cursor.execute(CREATE_TABLE_SQL)

        for index_sql in CREATE_INDEXES_SQL:
            cursor.execute(index_sql)

        # Clear this line if you want to append instead of replacing existing recipes.
        cursor.execute(f"TRUNCATE TABLE {TABLE_NAME} RESTART IDENTITY;")

        execute_values(cursor, INSERT_SQL, recipe_rows, page_size=100)

        connection.commit()

        cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME};")
        total_rows = cursor.fetchone()[0]

        print(f"Inserted {total_rows} recipes into '{TABLE_NAME}' successfully.")

        cursor.execute(f"""
            SELECT cuisine_area, COUNT(*)
            FROM {TABLE_NAME}
            GROUP BY cuisine_area
            ORDER BY cuisine_area;
        """)

        print("\nRecipes by cuisine area:")
        for cuisine_area, count in cursor.fetchall():
            print(f"- {cuisine_area}: {count}")

    except Exception as error:
        if connection:
            connection.rollback()
        print("Database setup/import failed:")
        print(error)
        sys.exit(1)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("\nDatabase connection closed.")


if __name__ == "__main__":
    main()
