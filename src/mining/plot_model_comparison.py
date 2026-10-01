import pandas as pd
import matplotlib.pyplot as plt
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
    / "reports"
    / "results"
    / "model_comparison.csv"
)

FIGURES_DIR = (
    PROJECT_ROOT
    / "reports"
    / "figures"
)

FIGURES_DIR.mkdir(
    parents=True,
    exist_ok=True
)


OUTPUT_PATH = (
    FIGURES_DIR
    / "model_comparison.png"
)


# ---------------------------------------------------------
# Load model comparison results
# ---------------------------------------------------------

df = pd.read_csv(INPUT_PATH)

print("Model comparison data loaded successfully.")

print("\nData:")
print(df)


# ---------------------------------------------------------
# Create comparison chart
# ---------------------------------------------------------

metrics = [
    "Accuracy",
    "Precision",
    "Recall",
    "F1_Score",
    "ROC_AUC"
]

for metric in metrics:

    plt.figure(figsize=(9, 6))

    plt.bar(
        df["Model"],
        df[metric]
    )

    plt.title(
        f"Model Comparison - {metric}"
    )

    plt.xlabel("Model")

    plt.ylabel(metric)

    plt.ylim(0, 1)

    plt.xticks(
        rotation=15
    )

    plt.tight_layout()

    output_file = (
        FIGURES_DIR
        / f"model_comparison_{metric.lower()}.png"
    )

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"Saved: {output_file}"
    )


print("\nAll model comparison charts created successfully.")