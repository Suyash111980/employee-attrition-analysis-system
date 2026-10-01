import sqlite3
from pathlib import Path


# ---------------------------------------------------------
# Project root
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# ---------------------------------------------------------
# File paths
# ---------------------------------------------------------

DATABASE_PATH = (
    PROJECT_ROOT
    / "database"
    / "employee_attrition.db"
)

SQL_PATH = (
    PROJECT_ROOT
    / "sql"
    / "olap"
    / "08_warehouse_validation.sql"
)


# ---------------------------------------------------------
# Connect to SQLite
# ---------------------------------------------------------

connection = sqlite3.connect(DATABASE_PATH)

print("SQLite database connected successfully.")


# ---------------------------------------------------------
# Read SQL file
# ---------------------------------------------------------

sql_script = SQL_PATH.read_text(encoding="utf-8")


# ---------------------------------------------------------
# Execute validation queries separately
# ---------------------------------------------------------

queries = [
    (
        "Total Fact Records",
        """
        SELECT COUNT(*)
        FROM FactEmployeeAttrition;
        """
    ),

    (
        "Attrition Distribution",
        """
        SELECT
            AttritionFlag,
            COUNT(*) AS EmployeeCount
        FROM FactEmployeeAttrition
        GROUP BY AttritionFlag
        ORDER BY AttritionFlag;
        """
    ),

    (
        "Invalid Attrition Flags",
        """
        SELECT COUNT(*)
        FROM FactEmployeeAttrition
        WHERE AttritionFlag NOT IN (0, 1);
        """
    ),

    (
        "Invalid Employee Keys",
        """
        SELECT COUNT(*)
        FROM FactEmployeeAttrition f
        LEFT JOIN DimEmployee e
            ON f.EmployeeKey = e.EmployeeKey
        WHERE e.EmployeeKey IS NULL;
        """
    ),

    (
        "Invalid Job Keys",
        """
        SELECT COUNT(*)
        FROM FactEmployeeAttrition f
        LEFT JOIN DimJob j
            ON f.JobKey = j.JobKey
        WHERE j.JobKey IS NULL;
        """
    ),

    (
        "Invalid Department Keys",
        """
        SELECT COUNT(*)
        FROM FactEmployeeAttrition f
        LEFT JOIN DimDepartment d
            ON f.DepartmentKey = d.DepartmentKey
        WHERE d.DepartmentKey IS NULL;
        """
    ),

    (
        "Invalid Satisfaction Keys",
        """
        SELECT COUNT(*)
        FROM FactEmployeeAttrition f
        LEFT JOIN DimSatisfaction s
            ON f.SatisfactionKey = s.SatisfactionKey
        WHERE s.SatisfactionKey IS NULL;
        """
    ),

    (
        "Invalid WorkLife Keys",
        """
        SELECT COUNT(*)
        FROM FactEmployeeAttrition f
        LEFT JOIN DimWorkLife w
            ON f.WorkLifeKey = w.WorkLifeKey
        WHERE w.WorkLifeKey IS NULL;
        """
    )
]


# ---------------------------------------------------------
# Run validation
# ---------------------------------------------------------

print("\nWarehouse Validation")
print("=" * 60)

for name, query in queries:

    result = connection.execute(query).fetchall()

    print(f"\n{name}:")
    
    for row in result:
        print(row)


# ---------------------------------------------------------
# Close connection
# ---------------------------------------------------------

connection.close()

print("\nWarehouse validation completed successfully.")