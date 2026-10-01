import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)


# ---------------------------------------------------------
# Project root
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# ---------------------------------------------------------
# Dataset path
# ---------------------------------------------------------

ML_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "employee_attrition_ml.csv"
)


# ---------------------------------------------------------
# Load dataset
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


print("\nTraining data:", X_train.shape)
print("Testing data:", X_test.shape)


# ---------------------------------------------------------
# Preprocessing
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


# ---------------------------------------------------------
# Decision Tree model
# ---------------------------------------------------------

model = DecisionTreeClassifier(
    class_weight="balanced",
    random_state=42,
    max_depth=5
)


# ---------------------------------------------------------
# Create ML pipeline
# ---------------------------------------------------------

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# ---------------------------------------------------------
# Train model
# ---------------------------------------------------------

print("\nTraining Decision Tree model...")

pipeline.fit(X_train, y_train)

print("Model training completed successfully.")


# ---------------------------------------------------------
# Predictions
# ---------------------------------------------------------

y_pred = pipeline.predict(X_test)

y_probability = pipeline.predict_proba(X_test)[:, 1]


# ---------------------------------------------------------
# Evaluation metrics
# ---------------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

roc_auc = roc_auc_score(
    y_test,
    y_probability
)


# ---------------------------------------------------------
# Display results
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("DECISION TREE RESULTS")
print("=" * 60)

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1-Score : {f1:.4f}")
print(f"ROC-AUC  : {roc_auc:.4f}")


# ---------------------------------------------------------
# Confusion Matrix
# ---------------------------------------------------------

cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:")
print(cm)


# ---------------------------------------------------------
# Classification Report
# ---------------------------------------------------------

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "No Attrition",
            "Attrition"
        ],
        zero_division=0
    )
)