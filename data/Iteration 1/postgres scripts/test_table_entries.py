"""
Health Insights Table Check Script

This script connects to PostgreSQL/RDS and prints sample rows from the
HealthyKids health insight tables.

Main responsibilities:
- Connects to the PostgreSQL database using psycopg2.
- Reads sample rows from the BMI, sleep, and physical inactivity tables.
- Prints up to 10 rows from each table for verification.
- Closes the cursor and database connection after completion.

Required variables expected before running:
- DB_HOST
- DB_NAME
- DB_USER
- DB_PASS
"""

import psycopg2
import pandas as pd
from pathlib import Path


# Open a connection to the PostgreSQL/RDS database.
connection = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=5432
    )

print("Connected successfully")

# Create a cursor so SQL commands can be executed.
cursor = connection.cursor()


# Read a small sample of BMI insight rows.
cursor.execute("SELECT * FROM bmi_5_17 LIMIT 10;")
rows = cursor.fetchall()

# Print each BMI sample row.
for row in rows:
    print(row)


# Read a small sample of sleep insight rows.
cursor.execute("SELECT * FROM sleep_weekend_week LIMIT 10;")
rows = cursor.fetchall()

# Print each sleep sample row.
for row in rows:
    print(row)


# Read a small sample of physical inactivity insight rows.
cursor.execute("SELECT * FROM physical_inactivity LIMIT 10;")
rows = cursor.fetchall()

# Print each physical inactivity sample row.
for row in rows:
    print(row)


# Close database resources after the script finishes.
cursor.close()
connection.close()