"""
Recipe Database Import Script

This script creates a PostgreSQL/RDS recipes table and imports recipe data
from a CSV file into the database.

Main responsibilities:
- Reads recipe data from a CSV file.
- Validates that the required CSV columns exist.
- Creates the recipes table if it does not already exist.
- Creates useful indexes for recipe filtering/searching.
- Clears existing recipe data before importing new rows.
- Inserts recipe records in batches using execute_values.
- Prints a short import summary after completion.

Required environment variables:
- DB_HOST
- DB_NAME
- DB_USER
- DB_PASS
- DB_PORT

Optional environment variable:
- CSV_FILE

Expected CSV columns:
- name
- area
- category
- ingredients
- steps
"""

import os
import csv
import sys
import psycopg2
from psycopg2.extras import execute_values


# CSV file path can be provided through the CSV_FILE environment variable.
CSV_FILE = os.getenv("CSV_FILE", "Multi_Cuisine_Recipe_Dataset.numbers")

# Database table name used for storing recipes.
TABLE_NAME = "recipes"


# SQL statement for creating the recipes table if it does not already exist.
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

# Batch insert statement used by psycopg2 execute_values.
INSERT_SQL = f"""
INSERT INTO {TABLE_NAME}
(recipe_name, cuisine_area, category, ingredients, steps)
VALUES %s;
"""


def validate_config():
    """
    Checks whether all required database configuration values are available.

    If any required environment variable is missing or still uses a placeholder,
    the script stops before attempting to connect to the database.
    """
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
    """
    Reads recipe rows from the CSV file and converts them into tuples ready for insertion.

    The function also validates that the CSV has the required column names before
    importing any data.
    """
    if not os.path.exists(csv_file):
        print(f"CSV file not found: {csv_file}")
        print("Place Multi_Cuisine_Recipe_Dataset.csv in the same folder as this script,")
        print("or set CSV_FILE=/path/to/Multi_Cuisine_Recipe_Dataset.csv")
        sys.exit(1)

    rows = []

    # utf-8-sig handles CSV files that may include a UTF-8 BOM at the start.
    with open(csv_file, mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        # Required CSV columns expected by the import script.
        expected_columns = {"name", "area", "category", "ingredients", "steps"}
        actual_columns = set(reader.fieldnames or [])

        # Stop early if the dataset structure does not match the expected format.
        if not expected_columns.issubset(actual_columns):
            print("CSV columns do not match the expected format.")
            print("Expected:", sorted(expected_columns))
            print("Found:", sorted(actual_columns))
            sys.exit(1)

        # Convert each CSV row into the exact column order used by INSERT_SQL.
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
    """
    Runs the full database setup and recipe import process.

    The process validates config, reads the CSV, connects to PostgreSQL/RDS,
    creates the table/indexes, replaces existing recipe data, inserts new rows,
    and prints a summary.
    """
    validate_config()
    recipe_rows = read_recipe_csv(CSV_FILE)

    if not recipe_rows:
        print("No recipe rows found in the CSV.")
        return

    connection = None
    cursor = None

    try:
        # Connect to the PostgreSQL/RDS database using the configured credentials.
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

        # Create the recipes table if needed.
        cursor.execute(CREATE_TABLE_SQL)

        # Create indexes used for faster filtering by cuisine, category, and recipe name.
        for index_sql in CREATE_INDEXES_SQL:
            cursor.execute(index_sql)

        # Clear this line if you want to append instead of replacing existing recipes.
        cursor.execute(f"TRUNCATE TABLE {TABLE_NAME} RESTART IDENTITY;")

        # Insert all recipe rows efficiently in batches.
        execute_values(cursor, INSERT_SQL, recipe_rows, page_size=100)

        connection.commit()

        # Confirm how many rows exist after import.
        cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME};")
        total_rows = cursor.fetchone()[0]

        print(f"Inserted {total_rows} recipes into '{TABLE_NAME}' successfully.")

        # Print a simple summary grouped by cuisine area.
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
        # Roll back the transaction if anything fails during setup or import.
        if connection:
            connection.rollback()
        print("Database setup/import failed:")
        print(error)
        sys.exit(1)

    finally:
        # Always close database resources after the script finishes.
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("\nDatabase connection closed.")


# Runs the import process only when this file is executed directly.
if __name__ == "__main__":
    main()