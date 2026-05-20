"""
Parent Profiles Table Setup Script

This script connects to PostgreSQL/RDS, creates the parent_profiles table,
and prints existing rows for verification.

Main responsibilities:
- Connects to the PostgreSQL database using psycopg2.
- Creates the parent_profiles table.
- Stores parent, child, quiz, recommendation, and dashboard data.
- Uses JSONB fields for list/object values such as habits, concerns, recommendations, and daily plans.
- Adds created_at and updated_at timestamps.
- Commits the table creation operation.
- Prints all existing parent_profiles rows for checking.
- Closes the cursor and database connection after completion.

Required variables expected before running:
- DB_HOTS
- DB_NAME
- DN_USER
- DB_PASS
"""

import psycopg2


# Open a connection to the PostgreSQL/RDS database.
connection = psycopg2.connect(
        host=DB_HOTS,
        database=DB_NAME,
        user=DN_USER,
        password=DB_PASS,
        port=5432
    )

print("Connected successfully")

# Create a cursor so SQL commands can be executed.
cursor = connection.cursor()

# Create the parent_profiles table used to store saved family plans and dashboard progress.
cursor.execute("""
        CREATE TABLE parent_profiles (
  id BIGSERIAL PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  parent_name VARCHAR(100),
  child_name VARCHAR(100),
  age_range VARCHAR(30),
  routine_type VARCHAR(100),
  habits JSONB NOT NULL DEFAULT '[]'::jsonb,
  concerns JSONB NOT NULL DEFAULT '[]'::jsonb,
  struggle TEXT,
  confidence VARCHAR(100),
  support_style VARCHAR(100),
  recommendations JSONB NOT NULL DEFAULT '[]'::jsonb,
  daily_plan JSONB NOT NULL DEFAULT '{}'::jsonb,
  progress_items JSONB NOT NULL DEFAULT '[]'::jsonb,
  next_action TEXT,
  mission TEXT,
  streak_days INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
    """)
connection.commit()


# Read all rows to confirm that the table exists and can be queried.
cursor.execute("SELECT * FROM parent_profiles;")
rows = cursor.fetchall()

# Print each existing parent profile record for verification.
for row in rows:
    print(row)


# Close database resources after the script finishes.
cursor.close()
connection.close()