import sqlite3
from pathlib import Path


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_PATH = (
    PROJECT_ROOT
    / "database"
    / "employee_attrition.db"
)


# Connect to database
connection = sqlite3.connect(DATABASE_PATH)

# Enable foreign keys
connection.execute("PRAGMA foreign_keys = ON;")

print("SQLite database connected successfully.")


# ---------------------------------------------------------
# 1. Load DimEmployee
# ---------------------------------------------------------

connection.execute("""
INSERT OR IGNORE INTO DimEmployee (
    EmployeeNumber,
    Age,
    Gender,
    MaritalStatus,
    EducationLevel,
    EducationField
)
SELECT
    EmployeeNumber,
    Age,
    Gender,
    MaritalStatus,
    Education,
    EducationField
FROM stg_employee_attrition;
""")

print("DimEmployee loaded successfully.")


# ---------------------------------------------------------
# 2. Load DimJob
# ---------------------------------------------------------

connection.execute("""
INSERT INTO DimJob (
    JobRole,
    JobLevel,
    BusinessTravel,
    OverTime
)
SELECT DISTINCT
    JobRole,
    JobLevel,
    BusinessTravel,
    OverTime
FROM stg_employee_attrition;
""")

print("DimJob loaded successfully.")


# ---------------------------------------------------------
# 3. Load DimDepartment
# ---------------------------------------------------------

connection.execute("""
INSERT OR IGNORE INTO DimDepartment (
    DepartmentName
)
SELECT DISTINCT
    Department
FROM stg_employee_attrition;
""")

print("DimDepartment loaded successfully.")


# ---------------------------------------------------------
# 4. Load DimSatisfaction
# ---------------------------------------------------------

connection.execute("""
INSERT INTO DimSatisfaction (
    EnvironmentSatisfaction,
    JobSatisfaction,
    JobInvolvement,
    RelationshipSatisfaction
)
SELECT DISTINCT
    EnvironmentSatisfaction,
    JobSatisfaction,
    JobInvolvement,
    RelationshipSatisfaction
FROM stg_employee_attrition;
""")

print("DimSatisfaction loaded successfully.")


# ---------------------------------------------------------
# 5. Load DimWorkLife
# ---------------------------------------------------------

connection.execute("""
INSERT INTO DimWorkLife (
    WorkLifeBalance,
    TrainingTimesLastYear,
    StockOptionLevel
)
SELECT DISTINCT
    WorkLifeBalance,
    TrainingTimesLastYear,
    StockOptionLevel
FROM stg_employee_attrition;
""")

print("DimWorkLife loaded successfully.")


# Commit changes
connection.commit()


# ---------------------------------------------------------
# Verify dimension row counts
# ---------------------------------------------------------

tables = [
    "DimEmployee",
    "DimJob",
    "DimDepartment",
    "DimSatisfaction",
    "DimWorkLife"
]

print("\nDimension table row counts:")

for table in tables:
    count = connection.execute(
        f"SELECT COUNT(*) FROM {table};"
    ).fetchone()[0]

    print(f"{table}: {count}")


# Close connection
connection.close()

print("\nDimension loading completed successfully.")