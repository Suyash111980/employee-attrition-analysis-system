import sqlite3
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "database" / "employee_attrition.db"
OUTPUT_DIR = PROJECT_ROOT / "dashboard" / "powerbi_data"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

tables = [
    "DimEmployee",
    "DimJob",
    "DimDepartment",
    "DimSatisfaction",
    "DimWorkLife",
    "FactEmployeeAttrition"
]

connection = sqlite3.connect(DB_PATH)

print("SQLite database connected successfully.")
print("Database:", DB_PATH)

for table in tables:

    query = f"SELECT * FROM {table}"

    df = pd.read_sql_query(query, connection)

    output_path = OUTPUT_DIR / f"{table}.csv"

    df.to_csv(output_path, index=False)

    print(f"{table}: {len(df)} rows exported.")

connection.close()

print("\nPower BI data export completed successfully.")
print("Output folder:", OUTPUT_DIR)