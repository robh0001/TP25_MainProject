import psycopg2
import pandas as pd
import pg8000
from pathlib import Path


DB_CONFIG = {
    "host": DB_HOTS,
    "port": 5432,
    "database": DB_NAME,
    "user": DB_USER,
    "password": DB_PASS,
}

BASE_DIR = Path(__file__).resolve().parent

BMI_CSV = BASE_DIR / "bmi_5_17.csv"
SLEEP_CSV = BASE_DIR / "sleep_weekend_week.csv"
INACTIVITY_CSV = BASE_DIR / "physical_inactivity.csv"

def connect_db():
    return pg8000.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        database=DB_CONFIG["database"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
    )


def create_tables(conn):
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
    for query in queries:
        cursor.execute(query)
    conn.commit()
    cursor.close()


def clear_tables(conn):
    queries = [
        "TRUNCATE TABLE bmi_5_17 RESTART IDENTITY;",
        "TRUNCATE TABLE sleep_weekend_week RESTART IDENTITY;",
        "TRUNCATE TABLE physical_inactivity RESTART IDENTITY;",
    ]

    cursor = conn.cursor()
    for query in queries:
        cursor.execute(query)
    conn.commit()
    cursor.close()


def insert_bmi_data(conn, csv_path):
    df = pd.read_csv(csv_path)

    cursor = conn.cursor()
    insert_query = """
        INSERT INTO bmi_5_17 (bmi_group, bmi_5_17_years)
        VALUES (%s, %s);
    """

    for _, row in df.iterrows():
        cursor.execute(insert_query, (row["bmi_group"], row["bmi_5_17_years"]))

    conn.commit()
    cursor.close()


def insert_sleep_data(conn, csv_path):
    df = pd.read_csv(csv_path)

    cursor = conn.cursor()
    insert_query = """
        INSERT INTO sleep_weekend_week (category, value_5_17)
        VALUES (%s, %s);
    """

    for _, row in df.iterrows():
        cursor.execute(insert_query, (row["category"], row["value_5_17"]))

    conn.commit()
    cursor.close()


def insert_physical_inactivity_data(conn, csv_path):
    df = pd.read_csv(csv_path)

    cursor = conn.cursor()
    insert_query = """
        INSERT INTO physical_inactivity (category, section_heading, value_5_17)
        VALUES (%s, %s, %s);
    """

    for _, row in df.iterrows():
        cursor.execute(
            insert_query,
            (row["category"], row["section_heading"], row["value_5_17"])
        )

    conn.commit()
    cursor.close()


def print_counts(conn):
    cursor = conn.cursor()

    tables = [
        "bmi_5_17",
        "sleep_weekend_week",
        "physical_inactivity",
    ]

    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table};")
        count = cursor.fetchone()[0]
        print(f"{table}: {count} rows inserted")

    cursor.close()


def main():
    for file_path in [BMI_CSV, SLEEP_CSV, INACTIVITY_CSV]:
        if not file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")

    conn = None
    try:
        conn = connect_db()
        print("Connected to RDS successfully.")

        create_tables(conn)
        print("Tables created successfully.")

        clear_tables(conn)
        print("Existing data cleared.")

        insert_bmi_data(conn, BMI_CSV)
        insert_sleep_data(conn, SLEEP_CSV)
        insert_physical_inactivity_data(conn, INACTIVITY_CSV)

        print("CSV data inserted successfully.")
        print_counts(conn)

    except Exception as e:
        print("Error:", e)
    finally:
        if conn:
            conn.close()
            print("Connection closed.")


if __name__ == "__main__":
    main()