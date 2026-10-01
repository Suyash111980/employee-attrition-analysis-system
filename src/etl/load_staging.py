import sqlite3
import pandas as pd
from pathlib import Path


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# File paths
CSV_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "employee_attrition_cleaned.csv"
)

DATABASE_PATH = (
    PROJECT_ROOT
    / "database"
    / "employee_attrition.db"
)


# Load cleaned CSV
df = pd.read_csv(CSV_PATH)

print("Cleaned CSV loaded successfully.")
print("Rows:", len(df))
print("Columns:", len(df.columns))


# Connect to SQLite database
connection = sqlite3.connect(DATABASE_PATH)

print("SQLite database connected successfully.")


# Load data into staging table
df.to_sql(
    "stg_employee_attrition",
    connection,
    if_exists="replace",
    index=False
)

print("Staging table created successfully.")


# Verify staging table
staging_count = connection.execute("""
SELECT COUNT(*)
FROM stg_employee_attrition;
""").fetchone()[0]

print("Rows in staging table:", staging_count)


# Close connection
connection.close()

print("Staging load completed successfully.")