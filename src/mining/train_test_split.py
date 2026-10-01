import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# ---------------------------------------------------------
# Project root
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# ---------------------------------------------------------
# File path
# ---------------------------------------------------------

ML_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "employee_attrition_ml.csv"
)


# ---------------------------------------------------------
# Load ML dataset
# ---------------------------------------------------------

df = pd.read_csv(ML_DATA_PATH)

print("ML dataset loaded successfully.")
print("Dataset shape:", df.shape)


# ---------------------------------------------------------
# Separate features and target
# ---------------------------------------------------------

X = df.drop(columns=["Attrition"])
y = df["Attrition"]


# ---------------------------------------------------------
# Identify feature types
# ---------------------------------------------------------

categorical_features = X.select_dtypes(
    include=["object", "str"]
).columns.tolist()

numerical_features = X.select_dtypes(
    exclude=["object", "str"]
).columns.tolist()


print("\nNumber of numerical features:", len(numerical_features))
print("Number of categorical features:", len(categorical_features))


# ---------------------------------------------------------
# Train-test split
# ---------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)


# ---------------------------------------------------------
# Display split information
# ---------------------------------------------------------

print("\nTrain/Test Split")
print("-" * 50)

print("Training features:", X_train.shape)
print("Testing features:", X_test.shape)

print("Training target:", y_train.shape)
print("Testing target:", y_test.shape)


# ---------------------------------------------------------
# Display target distribution
# ---------------------------------------------------------

print("\nTraining target distribution:")
print(y_train.value_counts().sort_index())

print("\nTesting target distribution:")
print(y_test.value_counts().sort_index())


# ---------------------------------------------------------
# Create preprocessing pipeline
# ---------------------------------------------------------

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numerical",
            StandardScaler(),
            numerical_features
        ),
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            ),
            categorical_features
        )
    ]
)


print("\nPreprocessing pipeline created successfully.")

print("\nNumerical preprocessing:")
print("StandardScaler")

print("\nCategorical preprocessing:")
print("OneHotEncoder(handle_unknown='ignore')")


# ---------------------------------------------------------
# Fit preprocessing ONLY on training data
# ---------------------------------------------------------

X_train_processed = preprocessor.fit_transform(X_train)

X_test_processed = preprocessor.transform(X_test)


# ---------------------------------------------------------
# Verify processed data
# ---------------------------------------------------------

print("\nProcessed training data shape:", X_train_processed.shape)
print("Processed testing data shape:", X_test_processed.shape)

print("\nPreprocessing completed successfully.")