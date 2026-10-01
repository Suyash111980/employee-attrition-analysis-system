import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# Project root
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# ---------------------------------------------------------
# File paths
# ---------------------------------------------------------

INPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "employee_attrition_cleaned.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "employee_attrition_ml.csv"
)


# ---------------------------------------------------------
# Load cleaned dataset
# ---------------------------------------------------------

df = pd.read_csv(INPUT_PATH)

print("Cleaned dataset loaded successfully.")
print("Original shape:", df.shape)


# ---------------------------------------------------------
# Convert target variable
# ---------------------------------------------------------

df["Attrition"] = df["Attrition"].map({
    "No": 0,
    "Yes": 1
})


# ---------------------------------------------------------
# Remove EmployeeNumber
# ---------------------------------------------------------

# EmployeeNumber is an identifier, not a predictive feature.
df = df.drop(columns=["EmployeeNumber"])


# ---------------------------------------------------------
# Separate features and target
# ---------------------------------------------------------

X = df.drop(columns=["Attrition"])
y = df["Attrition"]


# ---------------------------------------------------------
# Display ML dataset information
# ---------------------------------------------------------

print("\nML feature shape:", X.shape)
print("Target shape:", y.shape)

print("\nTarget distribution:")
print(y.value_counts().sort_index())

print("\nTarget percentages:")
print(
    (y.value_counts(normalize=True).sort_index() * 100).round(2)
)


# ---------------------------------------------------------
# Identify feature types
# ---------------------------------------------------------

categorical_features = X.select_dtypes(
    include=["object"]
).columns.tolist()

numerical_features = X.select_dtypes(
    exclude=["object"]
).columns.tolist()


print("\nCategorical features:")
print(categorical_features)

print("\nNumerical features:")
print(numerical_features)


# ---------------------------------------------------------
# Save ML dataset
# ---------------------------------------------------------

df.to_csv(OUTPUT_PATH, index=False)

print("\nML dataset saved successfully.")
print("Saved to:", OUTPUT_PATH)