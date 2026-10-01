import pandas as pd
from pathlib import Path

from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.cluster import KMeans


# ---------------------------------------------------------
# Project root
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

ML_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "employee_attrition_ml.csv"
)

RESULTS_DIR = PROJECT_ROOT / "reports" / "results"

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ---------------------------------------------------------
# Load dataset
# ---------------------------------------------------------

df = pd.read_csv(ML_DATA_PATH)

print("ML dataset loaded successfully.")
print("Dataset shape:", df.shape)


# ---------------------------------------------------------
# Keep original data for profiling
# ---------------------------------------------------------

profile_df = df.copy()


# ---------------------------------------------------------
# Remove target from clustering
# ---------------------------------------------------------

X = df.drop(
    columns=["Attrition"]
)


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
# Transform data
# ---------------------------------------------------------

X_processed = preprocessor.fit_transform(X)

print("\nProcessed clustering data shape:")
print(X_processed.shape)


# ---------------------------------------------------------
# K-Means with K = 2
# ---------------------------------------------------------

kmeans = KMeans(
    n_clusters=2,
    random_state=42,
    n_init=10
)


cluster_labels = kmeans.fit_predict(
    X_processed
)


# ---------------------------------------------------------
# Add cluster labels to profile dataset
# ---------------------------------------------------------

profile_df["Cluster"] = cluster_labels


print("\nK-Means clustering completed successfully.")


# ---------------------------------------------------------
# Cluster sizes
# ---------------------------------------------------------

cluster_sizes = (
    profile_df["Cluster"]
    .value_counts()
    .sort_index()
)


print("\nCluster Sizes")
print("-" * 40)

for cluster, count in cluster_sizes.items():
    print(
        f"Cluster {cluster}: {count} employees"
    )


# ---------------------------------------------------------
# Numerical cluster profile
# ---------------------------------------------------------

profile_columns = [
    "Age",
    "MonthlyIncome",
    "JobLevel",
    "JobSatisfaction",
    "WorkLifeBalance",
    "TotalWorkingYears",
    "YearsAtCompany",
    "DistanceFromHome",
    "NumCompaniesWorked"
]


cluster_profile = (
    profile_df
    .groupby("Cluster")[profile_columns]
    .mean()
    .round(2)
)


print("\nNumerical Cluster Profile")
print("=" * 80)

print(cluster_profile)


# ---------------------------------------------------------
# Attrition distribution by cluster
# ---------------------------------------------------------

attrition_cluster = pd.crosstab(
    profile_df["Cluster"],
    profile_df["Attrition"],
    normalize="index"
) * 100


attrition_cluster = attrition_cluster.round(2)


print("\nAttrition Distribution by Cluster (%)")
print("=" * 80)

print(attrition_cluster)


# ---------------------------------------------------------
# Save cluster assignments
# ---------------------------------------------------------

cluster_output_path = (
    RESULTS_DIR
    / "employee_clusters.csv"
)


profile_df.to_csv(
    cluster_output_path,
    index=False
)


print(
    "\nCluster assignments saved to:"
)

print(cluster_output_path)


# ---------------------------------------------------------
# Save cluster profile
# ---------------------------------------------------------

profile_output_path = (
    RESULTS_DIR
    / "kmeans_cluster_profile.csv"
)


cluster_profile.to_csv(
    profile_output_path
)


print(
    "\nCluster profile saved to:"
)

print(profile_output_path)


# ---------------------------------------------------------
# Save attrition distribution
# ---------------------------------------------------------

attrition_output_path = (
    RESULTS_DIR
    / "kmeans_attrition_by_cluster.csv"
)


attrition_cluster.to_csv(
    attrition_output_path
)


print(
    "\nAttrition-by-cluster results saved to:"
)

print(attrition_output_path)


print(
    "\nK-Means clustering analysis completed successfully."
)