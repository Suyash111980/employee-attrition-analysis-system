import sqlite3
from pathlib import Path


# ---------------------------------------------------------
# Project root
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# ---------------------------------------------------------
# Database path
# ---------------------------------------------------------

DATABASE_PATH = (
    PROJECT_ROOT
    / "database"
    / "employee_attrition.db"
)


# ---------------------------------------------------------
# Connect to SQLite database
# ---------------------------------------------------------

connection = sqlite3.connect(DATABASE_PATH)

print("SQLite database connected successfully.")


# =========================================================
# OLAP QUERY 1: Overall Attrition Summary
# =========================================================

query_overall = """
SELECT
    AttritionFlag,
    COUNT(*) AS EmployeeCount,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM FactEmployeeAttrition),
        2
    ) AS Percentage
FROM FactEmployeeAttrition
GROUP BY AttritionFlag
ORDER BY AttritionFlag;
"""


result_overall = connection.execute(query_overall).fetchall()


print("\nOverall Attrition Summary")
print("-" * 50)

print("AttritionFlag | EmployeeCount | Percentage")

for row in result_overall:
    print(row)


# =========================================================
# OLAP QUERY 2: Department-wise Attrition Analysis
# =========================================================

query_department = """
SELECT
    d.DepartmentName,
    COUNT(*) AS EmployeeCount,
    SUM(f.AttritionFlag) AS AttritionCount,
    ROUND(
        SUM(f.AttritionFlag) * 100.0 / COUNT(*),
        2
    ) AS AttritionRate
FROM FactEmployeeAttrition f
JOIN DimDepartment d
    ON f.DepartmentKey = d.DepartmentKey
GROUP BY d.DepartmentName
ORDER BY AttritionRate DESC;
"""


result_department = connection.execute(query_department).fetchall()


print("\nDepartment-wise Attrition Analysis")
print("-" * 70)

print(
    "Department | EmployeeCount | AttritionCount | AttritionRate"
)

for row in result_department:
    print(row)

# =========================================================
# OLAP QUERY 3: Job Role-wise Attrition Analysis
# =========================================================

query_job_role = """
SELECT
    d.DepartmentName,
    j.JobRole,
    COUNT(*) AS EmployeeCount,
    SUM(f.AttritionFlag) AS AttritionCount,
    ROUND(
        SUM(f.AttritionFlag) * 100.0 / COUNT(*),
        2
    ) AS AttritionRate
FROM FactEmployeeAttrition f
JOIN DimDepartment d
    ON f.DepartmentKey = d.DepartmentKey
JOIN DimJob j
    ON f.JobKey = j.JobKey
GROUP BY
    d.DepartmentName,
    j.JobRole
ORDER BY
    d.DepartmentName,
    AttritionRate DESC;
"""

result_job_role = connection.execute(query_job_role).fetchall()

print("\nJob Role-wise Attrition Analysis")
print("-" * 90)

print(
    "Department | JobRole | EmployeeCount | "
    "AttritionCount | AttritionRate"
)

for row in result_job_role:
    print(row)



# =========================================================
# OLAP QUERY 4: Overtime-wise Attrition Analysis
# =========================================================

query_overtime = """
SELECT
    j.OverTime,
    COUNT(*) AS EmployeeCount,
    SUM(f.AttritionFlag) AS AttritionCount,
    ROUND(
        SUM(f.AttritionFlag) * 100.0 / COUNT(*),
        2
    ) AS AttritionRate
FROM FactEmployeeAttrition f
JOIN DimJob j
    ON f.JobKey = j.JobKey
GROUP BY j.OverTime
ORDER BY AttritionRate DESC;
"""

result_overtime = connection.execute(query_overtime).fetchall()

print("\nOvertime-wise Attrition Analysis")
print("-" * 70)

print(
    "OverTime | EmployeeCount | "
    "AttritionCount | AttritionRate"
)

for row in result_overtime:
    print(row)    



# =========================================================
# OLAP QUERY 5: Job Level-wise Attrition Analysis
# =========================================================

query_job_level = """
SELECT
    j.JobLevel,
    COUNT(*) AS EmployeeCount,
    SUM(f.AttritionFlag) AS AttritionCount,
    ROUND(
        SUM(f.AttritionFlag) * 100.0 / COUNT(*),
        2
    ) AS AttritionRate,
    ROUND(
        AVG(f.MonthlyIncome),
        2
    ) AS AverageMonthlyIncome
FROM FactEmployeeAttrition f
JOIN DimJob j
    ON f.JobKey = j.JobKey
GROUP BY j.JobLevel
ORDER BY j.JobLevel;
"""

result_job_level = connection.execute(query_job_level).fetchall()

print("\nJob Level-wise Attrition Analysis")
print("-" * 90)

print(
    "JobLevel | EmployeeCount | AttritionCount | "
    "AttritionRate | AverageMonthlyIncome"
)

for row in result_job_level:
    print(row) 


# =========================================================
# OLAP QUERY 6: Job Satisfaction-wise Attrition Analysis
# =========================================================

query_satisfaction = """
SELECT
    s.JobSatisfaction,
    COUNT(*) AS EmployeeCount,
    SUM(f.AttritionFlag) AS AttritionCount,
    ROUND(
        SUM(f.AttritionFlag) * 100.0 / COUNT(*),
        2
    ) AS AttritionRate
FROM FactEmployeeAttrition f
JOIN DimSatisfaction s
    ON f.SatisfactionKey = s.SatisfactionKey
GROUP BY s.JobSatisfaction
ORDER BY s.JobSatisfaction;
"""

result_satisfaction = connection.execute(
    query_satisfaction
).fetchall()

print("\nJob Satisfaction-wise Attrition Analysis")
print("-" * 80)

print(
    "JobSatisfaction | EmployeeCount | "
    "AttritionCount | AttritionRate"
)

for row in result_satisfaction:
    print(row)      

# =========================================================
# OLAP QUERY 7: Work-Life Balance-wise Attrition Analysis
# =========================================================

query_worklife = """
SELECT
    w.WorkLifeBalance,
    COUNT(*) AS EmployeeCount,
    SUM(f.AttritionFlag) AS AttritionCount,
    ROUND(
        SUM(f.AttritionFlag) * 100.0 / COUNT(*),
        2
    ) AS AttritionRate
FROM FactEmployeeAttrition f
JOIN DimWorkLife w
    ON f.WorkLifeKey = w.WorkLifeKey
GROUP BY w.WorkLifeBalance
ORDER BY w.WorkLifeBalance;
"""

result_worklife = connection.execute(
    query_worklife
).fetchall()

print("\nWork-Life Balance-wise Attrition Analysis")
print("-" * 80)

print(
    "WorkLifeBalance | EmployeeCount | "
    "AttritionCount | AttritionRate"
)

for row in result_worklife:
    print(row)     
# ---------------------------------------------------------
# Close database connection
# ---------------------------------------------------------

connection.close()

print("\nOLAP analysis completed successfully.")