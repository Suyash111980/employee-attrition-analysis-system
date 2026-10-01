import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# Project root
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# ---------------------------------------------------------
# Results directory
# ---------------------------------------------------------

RESULTS_DIR = PROJECT_ROOT / "reports" / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# Actual model results from our experiments
# ---------------------------------------------------------

results = [
    {
        "Model": "Logistic Regression",
        "Accuracy": 0.7642,
        "Precision": 0.3721,
        "Recall": 0.6761,
        "F1_Score": 0.4800,
        "ROC_AUC": 0.8163
    },
    {
        "Model": "Decision Tree",
        "Accuracy": 0.7324,
        "Precision": 0.3206,
        "Recall": 0.5915,
        "F1_Score": 0.4158,
        "ROC_AUC": 0.6489
    },
    {
        "Model": "Random Forest",
        "Accuracy": 0.8254,
        "Precision": 0.4444,
        "Recall": 0.3380,
        "F1_Score": 0.3840,
        "ROC_AUC": 0.7785
    }
]


# ---------------------------------------------------------
# Create DataFrame
# ---------------------------------------------------------

comparison_df = pd.DataFrame(results)


# ---------------------------------------------------------
# Display comparison
# ---------------------------------------------------------

print("\nClassification Model Comparison")
print("=" * 80)

print(comparison_df.to_string(index=False))


# ---------------------------------------------------------
# Save results
# ---------------------------------------------------------

OUTPUT_PATH = RESULTS_DIR / "model_comparison.csv"

comparison_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\nModel comparison saved successfully.")
print("Saved to:", OUTPUT_PATH)