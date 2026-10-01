import pandas as pd
from pathlib import Path


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# File paths
RAW_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
)

PROCESSED_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "employee_attrition_cleaned.csv"
)


# Load the raw dataset
df = pd.read_csv(RAW_DATA_PATH)

print("Raw dataset loaded successfully.")
print("Original shape:", df.shape)
# Remove columns with no variation
constant_columns = [
    "EmployeeCount",
    "Over18",
    "StandardHours"
]

df = df.drop(columns=constant_columns)

print("Constant columns removed:", constant_columns)
print("Shape after removing constant columns:", df.shape)

print("\nRemaining columns:")
print(df.columns.tolist())

# Check for duplicate rows
duplicate_count = df.duplicated().sum()

print("Duplicate rows after preprocessing:", duplicate_count)

# Check for missing values
missing_values = df.isnull().sum().sum()

print("Total missing values after preprocessing:", missing_values)

# Save the cleaned dataset
df.to_csv(PROCESSED_DATA_PATH, index=False)

print("Cleaned dataset saved successfully.")
print("Saved to:", PROCESSED_DATA_PATH)