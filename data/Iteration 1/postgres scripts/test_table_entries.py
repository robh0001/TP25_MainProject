import psycopg2
import pandas as pd
from pathlib import Path


connection = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=5432
    )

print("Connected successfully")

cursor = connection.cursor()


cursor.execute("SELECT * FROM bmi_5_17 LIMIT 10;")
rows = cursor.fetchall()

for row in rows:
    print(row)


cursor.execute("SELECT * FROM sleep_weekend_week LIMIT 10;")
rows = cursor.fetchall()

for row in rows:
    print(row)


cursor.execute("SELECT * FROM physical_inactivity LIMIT 10;")
rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
connection.close()
