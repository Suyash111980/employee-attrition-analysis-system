import sqlite3
from pathlib import Path


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Database directory
DATABASE_DIR = PROJECT_ROOT / "database"

# Create database directory if it does not exist
DATABASE_DIR.mkdir(exist_ok=True)

# SQLite database path
DATABASE_PATH = DATABASE_DIR / "employee_attrition.db"

# Connect to SQLite
connection = sqlite3.connect(DATABASE_PATH)

# Enable foreign key support
connection.execute("PRAGMA foreign_keys = ON;")

print("SQLite database connection successful.")
print("Database path:", DATABASE_PATH)


# Create DimEmployee table
connection.execute("""
CREATE TABLE IF NOT EXISTS DimEmployee (
    EmployeeKey INTEGER PRIMARY KEY AUTOINCREMENT,
    EmployeeNumber INTEGER NOT NULL UNIQUE,
    Age INTEGER,
    Gender TEXT,
    MaritalStatus TEXT,
    EducationLevel INTEGER,
    EducationField TEXT
);
""")

connection.commit()

print("DimEmployee table created successfully.")


# Create DimJob table
connection.execute("""
CREATE TABLE IF NOT EXISTS DimJob (
    JobKey INTEGER PRIMARY KEY AUTOINCREMENT,
    JobRole TEXT,
    JobLevel INTEGER,
    BusinessTravel TEXT,
    OverTime TEXT
);
""")

connection.commit()

print("DimJob table created successfully.")


# Create DimDepartment table
connection.execute("""
CREATE TABLE IF NOT EXISTS DimDepartment (
    DepartmentKey INTEGER PRIMARY KEY AUTOINCREMENT,
    DepartmentName TEXT NOT NULL UNIQUE
);
""")

connection.commit()

print("DimDepartment table created successfully.")


# Create DimSatisfaction table
connection.execute("""
CREATE TABLE IF NOT EXISTS DimSatisfaction (
    SatisfactionKey INTEGER PRIMARY KEY AUTOINCREMENT,
    EnvironmentSatisfaction INTEGER,
    JobSatisfaction INTEGER,
    JobInvolvement INTEGER,
    RelationshipSatisfaction INTEGER
);
""")

connection.commit()

print("DimSatisfaction table created successfully.")


# Create DimWorkLife table
connection.execute("""
CREATE TABLE IF NOT EXISTS DimWorkLife (
    WorkLifeKey INTEGER PRIMARY KEY AUTOINCREMENT,
    WorkLifeBalance INTEGER,
    TrainingTimesLastYear INTEGER,
    StockOptionLevel INTEGER
);
""")

connection.commit()

print("DimWorkLife table created successfully.")




# Create FactEmployeeAttrition table
connection.execute("""
CREATE TABLE IF NOT EXISTS FactEmployeeAttrition (
    AttritionFactKey INTEGER PRIMARY KEY AUTOINCREMENT,

    EmployeeKey INTEGER NOT NULL,
    JobKey INTEGER NOT NULL,
    DepartmentKey INTEGER NOT NULL,
    SatisfactionKey INTEGER NOT NULL,
    WorkLifeKey INTEGER NOT NULL,

    AttritionFlag INTEGER NOT NULL,

    DailyRate INTEGER,
    HourlyRate INTEGER,
    MonthlyIncome INTEGER,
    MonthlyRate INTEGER,
    PercentSalaryHike INTEGER,

    DistanceFromHome INTEGER,
    NumCompaniesWorked INTEGER,
    TotalWorkingYears INTEGER,

    YearsAtCompany INTEGER,
    YearsInCurrentRole INTEGER,
    YearsSinceLastPromotion INTEGER,
    YearsWithCurrManager INTEGER,

    FOREIGN KEY (EmployeeKey)
        REFERENCES DimEmployee(EmployeeKey),

    FOREIGN KEY (JobKey)
        REFERENCES DimJob(JobKey),

    FOREIGN KEY (DepartmentKey)
        REFERENCES DimDepartment(DepartmentKey),

    FOREIGN KEY (SatisfactionKey)
        REFERENCES DimSatisfaction(SatisfactionKey),

    FOREIGN KEY (WorkLifeKey)
        REFERENCES DimWorkLife(WorkLifeKey)
);
""")

connection.commit()

print("FactEmployeeAttrition table created successfully.")



# Verify all tables in the database
tables = connection.execute("""
SELECT name
FROM sqlite_master
WHERE type = 'table'
ORDER BY name;
""").fetchall()

print("\nTables in database:")
for table in tables:
    print("-", table[0])


# Verify FactEmployeeAttrition foreign keys
foreign_keys = connection.execute("""
PRAGMA foreign_key_list(FactEmployeeAttrition);
""").fetchall()

print("\nForeign keys in FactEmployeeAttrition:")
for fk in foreign_keys:
    print(fk)


# Close database connection
connection.close()

print("\nDatabase schema verification completed.")