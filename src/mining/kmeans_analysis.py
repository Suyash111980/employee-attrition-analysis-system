import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


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
# Remove target and identifier
# ---------------------------------------------------------

X = df.drop(
    columns=["Attrition"]
)

print("\nClustering dataset shape:", X.shape)


# ---------------------------------------------------------
# Identify feature types
# ---------------------------------------------------------

categorical_features = X.select_dtypes(
    include=["object", "str"]
).columns.tolist()

numerical_features = X.select_dtypes(
    exclude=["object", "str"]
).columns.tolist()


print("\nNumerical features:", len(numerical_features))
print("Categorical features:", len(categorical_features))


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
# Transform clustering data
# ---------------------------------------------------------

X_processed = preprocessor.fit_transform(X)

print("\nProcessed clustering data shape:")
print(X_processed.shape)


# ---------------------------------------------------------
# Test different K values
# ---------------------------------------------------------

k_values = range(2, 9)

inertia_values = []
silhouette_values = []


print("\nTesting K values...")
print("-" * 60)

for k in k_values:

    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    cluster_labels = kmeans.fit_predict(
        X_processed
    )

    inertia = kmeans.inertia_

    silhouette = silhouette_score(
        X_processed,
        cluster_labels
    )

    inertia_values.append(inertia)
    silhouette_values.append(silhouette)

    print(
        f"K = {k} | "
        f"Inertia = {inertia:.2f} | "
        f"Silhouette Score = {silhouette:.4f}"
    )


# ---------------------------------------------------------
# Create reports/figures directory
# ---------------------------------------------------------

FIGURES_DIR = (
    PROJECT_ROOT
    / "reports"
    / "figures"
)

FIGURES_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ---------------------------------------------------------
# Elbow Method plot
# ---------------------------------------------------------

plt.figure(figsize=(9, 6))

plt.plot(
    list(k_values),
    inertia_values,
    marker="o"
)

plt.title(
    "K-Means Elbow Method"
)

plt.xlabel(
    "Number of Clusters (K)"
)

plt.ylabel(
    "Inertia"
)

plt.xticks(
    list(k_values)
)

plt.tight_layout()


ELBOW_PATH = (
    FIGURES_DIR
    / "kmeans_elbow.png"
)

plt.savefig(
    ELBOW_PATH,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


print(
    "\nElbow plot saved to:"
)

print(ELBOW_PATH)


# ---------------------------------------------------------
# Silhouette Score plot
# ---------------------------------------------------------

plt.figure(figsize=(9, 6))

plt.plot(
    list(k_values),
    silhouette_values,
    marker="o"
)

plt.title(
    "K-Means Silhouette Scores"
)

plt.xlabel(
    "Number of Clusters (K)"
)

plt.ylabel(
    "Silhouette Score"
)

plt.xticks(
    list(k_values)
)

plt.tight_layout()


SILHOUETTE_PATH = (
    FIGURES_DIR
    / "kmeans_silhouette.png"
)

plt.savefig(
    SILHOUETTE_PATH,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


print(
    "Silhouette plot saved to:"
)

print(SILHOUETTE_PATH)


# ---------------------------------------------------------
# Save diagnostic results
# ---------------------------------------------------------

diagnostics = pd.DataFrame({
    "K": list(k_values),
    "Inertia": inertia_values,
    "Silhouette_Score": silhouette_values
})


RESULTS_DIR = (
    PROJECT_ROOT
    / "reports"
    / "results"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


RESULTS_PATH = (
    RESULTS_DIR
    / "kmeans_diagnostics.csv"
)

diagnostics.to_csv(
    RESULTS_PATH,
    index=False
)


print(
    "\nK-Means diagnostic results saved to:"
)

print(RESULTS_PATH)


print(
    "\nK-Means diagnostic analysis completed successfully."
)