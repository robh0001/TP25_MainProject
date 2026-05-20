"""
Health Insights Data Import Script

This script creates and populates the HealthyKids health insight tables in
PostgreSQL/RDS using local CSV files.

Main responsibilities:
- Connects to PostgreSQL/RDS using pg8000.
- Locates CSV files from the same folder as this script.
- Creates BMI, sleep, and physical inactivity tables if they do not exist.
- Clears existing table data before importing new data.
- Reads CSV files using pandas.
- Inserts BMI, sleep, and inactivity records into the database.
- Prints row counts after import for verification.
- Closes the database connection after completion.

Required variables expected before running:
- DB_HOTS
- DB_NAME
- DB_USER
- DB_PASS

Required CSV files:
- bmi_5_17.csv
- sleep_weekend_week.csv
- physical_inactivity.csv
"""

import psycopg2
import pandas as pd
import pg8000
from pathlib import Path


# Database connection settings.
DB_CONFIG = {
    "host": DB_HOTS,
    "port": 5432,
    "database": DB_NAME,
    "user": DB_USER,
    "password": DB_PASS,
}

# Folder where this script is located.
BASE_DIR = Path(__file__).resolve().parent

# CSV file paths expected in the same folder as this script.
BMI_CSV = BASE_DIR / "bmi_5_17.csv"
SLEEP_CSV = BASE_DIR / "sleep_weekend_week.csv"
INACTIVITY_CSV = BASE_DIR / "physical_inactivity.csv"


def connect_db():
    """
    Creates and returns a PostgreSQL/RDS database connection using pg8000.
    """
    return pg8000.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        database=DB_CONFIG["database"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
    )


def create_tables(conn):
    """
    Creates the health insight tables if they do not already exist.

    These tables store BMI, sleep, and physical inactivity data used by the
    HealthyKids statistics or insights page.
    """
    queries = [
        """
        CREATE TABLE IF NOT EXISTS bmi_5_17 (
            id SERIAL PRIMARY KEY,
            bmi_group TEXT NOT NULL,
            bmi_5_17_years DOUBLE PRECISION
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS sleep_weekend_week (
            id SERIAL PRIMARY KEY,
            category TEXT NOT NULL,
            value_5_17 DOUBLE PRECISION
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS physical_inactivity (
            id SERIAL PRIMARY KEY,
            category TEXT NOT NULL,
            section_heading TEXT,
            value_5_17 DOUBLE PRECISION
        );
        """
    ]

    cursor = conn.cursor()

    # Run each CREATE TABLE statement.
    for query in queries:
        cursor.execute(query)

    conn.commit()
    cursor.close()


def clear_tables(conn):
    """
    Clears existing health insight data before importing fresh CSV data.

    RESTART IDENTITY resets the auto-incrementing primary key values.
    """
    queries = [
        "TRUNCATE TABLE bmi_5_17 RESTART IDENTITY;",
        "TRUNCATE TABLE sleep_weekend_week RESTART IDENTITY;",
        "TRUNCATE TABLE physical_inactivity RESTART IDENTITY;",
    ]

    cursor = conn.cursor()

    # Run each TRUNCATE statement.
    for query in queries:
        cursor.execute(query)

    conn.commit()
    cursor.close()


def insert_bmi_data(conn, csv_path):
    """
    Reads BMI CSV data and inserts it into the bmi_5_17 table.
    """
    df = pd.read_csv(csv_path)

    cursor = conn.cursor()
    insert_query = """
        INSERT INTO bmi_5_17 (bmi_group, bmi_5_17_years)
        VALUES (%s, %s);
    """

    # Insert each BMI row from the dataframe.
    for _, row in df.iterrows():
        cursor.execute(insert_query, (row["bmi_group"], row["bmi_5_17_years"]))

    conn.commit()
    cursor.close()


def insert_sleep_data(conn, csv_path):
    """
    Reads sleep CSV data and inserts it into the sleep_weekend_week table.
    """
    df = pd.read_csv(csv_path)

    cursor = conn.cursor()
    insert_query = """
        INSERT INTO sleep_weekend_week (category, value_5_17)
        VALUES (%s, %s);
    """

    # Insert each sleep category row from the dataframe.
    for _, row in df.iterrows():
        cursor.execute(insert_query, (row["category"], row["value_5_17"]))

    conn.commit()
    cursor.close()


def insert_physical_inactivity_data(conn, csv_path):
    """
    Reads physical inactivity CSV data and inserts it into the
    physical_inactivity table.
    """
    df = pd.read_csv(csv_path)

    cursor = conn.cursor()
    insert_query = """
        INSERT INTO physical_inactivity (category, section_heading, value_5_17)
        VALUES (%s, %s, %s);
    """

    # Insert each physical inactivity row from the dataframe.
    for _, row in df.iterrows():
        cursor.execute(
            insert_query,
            (row["category"], row["section_heading"], row["value_5_17"])
        )

    conn.commit()
    cursor.close()


def print_counts(conn):
    """
    Prints the number of rows inserted into each health insight table.
    """
    cursor = conn.cursor()

    tables = [
        "bmi_5_17",
        "sleep_weekend_week",
        "physical_inactivity",
    ]

    # Count rows in each imported table.
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table};")
        count = cursor.fetchone()[0]
        print(f"{table}: {count} rows inserted")

    cursor.close()


def main():
    """
    Runs the full CSV import process.

    The script checks that all CSV files exist, connects to the database,
    creates the required tables, clears old data, imports new data, and prints
    table counts for verification.
    """
    # Make sure all required CSV files are available before connecting.
    for file_path in [BMI_CSV, SLEEP_CSV, INACTIVITY_CSV]:
        if not file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")

    conn = None

    try:
        # Connect to PostgreSQL/RDS.
        conn = connect_db()
        print("Connected to RDS successfully.")

        # Create required tables.
        create_tables(conn)
        print("Tables created successfully.")

        # Clear old data before importing fresh CSV rows.
        clear_tables(conn)
        print("Existing data cleared.")

        # Import CSV data into each table.
        insert_bmi_data(conn, BMI_CSV)
        insert_sleep_data(conn, SLEEP_CSV)
        insert_physical_inactivity_data(conn, INACTIVITY_CSV)

        print("CSV data inserted successfully.")

        # Print row counts to confirm the import worked.
        print_counts(conn)

    except Exception as e:
        # Print any setup/import error.
        print("Error:", e)

    finally:
        # Always close the database connection after the script finishes.
        if conn:
            conn.close()
            print("Connection closed.")


# Run the import only when this file is executed directly.
if __name__ == "__main__":
    main()