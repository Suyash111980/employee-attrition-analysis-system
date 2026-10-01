import sqlite3
from pathlib import Path


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_PATH = (
    PROJECT_ROOT
    / "database"
    / "employee_attrition.db"
)


# Connect to SQLite
connection = sqlite3.connect(DATABASE_PATH)

# Enable foreign keys
connection.execute("PRAGMA foreign_keys = ON;")

print("SQLite database connected successfully.")


# ---------------------------------------------------------
# Load FactEmployeeAttrition
# ---------------------------------------------------------

connection.execute("""
INSERT INTO FactEmployeeAttrition (
    EmployeeKey,
    JobKey,
    DepartmentKey,
    SatisfactionKey,
    WorkLifeKey,
    AttritionFlag,
    DailyRate,
    HourlyRate,
    MonthlyIncome,
    MonthlyRate,
    PercentSalaryHike,
    DistanceFromHome,
    NumCompaniesWorked,
    TotalWorkingYears,
    YearsAtCompany,
    YearsInCurrentRole,
    YearsSinceLastPromotion,
    YearsWithCurrManager
)
SELECT
    e.EmployeeKey,
    j.JobKey,
    d.DepartmentKey,
    s.SatisfactionKey,
    w.WorkLifeKey,

    CASE
        WHEN st.Attrition = 'Yes' THEN 1
        ELSE 0
    END AS AttritionFlag,

    st.DailyRate,
    st.HourlyRate,
    st.MonthlyIncome,
    st.MonthlyRate,
    st.PercentSalaryHike,
    st.DistanceFromHome,
    st.NumCompaniesWorked,
    st.TotalWorkingYears,
    st.YearsAtCompany,
    st.YearsInCurrentRole,
    st.YearsSinceLastPromotion,
    st.YearsWithCurrManager

FROM stg_employee_attrition st

INNER JOIN DimEmployee e
    ON st.EmployeeNumber = e.EmployeeNumber

INNER JOIN DimJob j
    ON st.JobRole = j.JobRole
    AND st.JobLevel = j.JobLevel
    AND st.BusinessTravel = j.BusinessTravel
    AND st.OverTime = j.OverTime

INNER JOIN DimDepartment d
    ON st.Department = d.DepartmentName

INNER JOIN DimSatisfaction s
    ON st.EnvironmentSatisfaction = s.EnvironmentSatisfaction
    AND st.JobSatisfaction = s.JobSatisfaction
    AND st.JobInvolvement = s.JobInvolvement
    AND st.RelationshipSatisfaction = s.RelationshipSatisfaction

INNER JOIN DimWorkLife w
    ON st.WorkLifeBalance = w.WorkLifeBalance
    AND st.TrainingTimesLastYear = w.TrainingTimesLastYear
    AND st.StockOptionLevel = w.StockOptionLevel;
""")


connection.commit()

print("FactEmployeeAttrition loaded successfully.")


# ---------------------------------------------------------
# Verify fact table
# ---------------------------------------------------------

fact_count = connection.execute("""
SELECT COUNT(*)
FROM FactEmployeeAttrition;
""").fetchone()[0]

print("Rows in FactEmployeeAttrition:", fact_count)


# ---------------------------------------------------------
# Verify AttritionFlag
# ---------------------------------------------------------

attrition_counts = connection.execute("""
SELECT
    AttritionFlag,
    COUNT(*) AS EmployeeCount
FROM FactEmployeeAttrition
GROUP BY AttritionFlag
ORDER BY AttritionFlag;
""").fetchall()

print("\nAttritionFlag distribution:")

for flag, count in attrition_counts:
    print(f"AttritionFlag {flag}: {count}")


# ---------------------------------------------------------
# Verify missing foreign keys
# ---------------------------------------------------------

null_foreign_keys = connection.execute("""
SELECT COUNT(*)
FROM FactEmployeeAttrition
WHERE EmployeeKey IS NULL
   OR JobKey IS NULL
   OR DepartmentKey IS NULL
   OR SatisfactionKey IS NULL
   OR WorkLifeKey IS NULL;
""").fetchone()[0]

print("\nRows with missing foreign keys:", null_foreign_keys)


# Close connection
connection.close()

print("\nFact table loading completed successfully.")