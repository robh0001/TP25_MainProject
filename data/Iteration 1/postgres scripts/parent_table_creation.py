import psycopg2

connection = psycopg2.connect(
        host=DB_HOTS,
        database=DB_NAME,
        user=DN_USER,
        password=DB_PASS,
        port=5432
    )

print("Connected successfully")

cursor = connection.cursor()

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


cursor.execute("SELECT * FROM parent_profiles;")
rows = cursor.fetchall()

for row in rows:
    print(row)


cursor.close()
connection.close()
