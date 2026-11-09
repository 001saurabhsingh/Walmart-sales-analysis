"""
Walmart Sales Analysis - Macroeconomic Factors & Correlation
Tests the linear correlation between weekly sales and economic variables.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from data_preprocessing import load_and_clean_data

OUTPUT_DIR = Path("visualizations")
OUTPUT_DIR.mkdir(exist_ok=True)


def analyze_correlations(df):
    numeric_cols = df.select_dtypes(include="number")
    corr_matrix = numeric_cols.corr()

    # Heatmap of all numeric factors
    plt.figure(figsize=(9, 7))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", center=0, cbar=True)
    plt.title("Correlation Matrix: Sales vs External Economic Factors", fontsize=13, pad=12)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "07_correlation_heatmap.png", dpi=150)
    plt.close()
    print("Saved 07_correlation_heatmap.png")

    # Focus specifically on correlations with Weekly_Sales
    factors = ["Temperature", "Fuel_Price", "CPI", "Unemployment"]
    sales_corr = corr_matrix["Weekly_Sales"][factors].sort_values()

    print("\n--- Correlation with Weekly Sales ---")
    for factor, value in sales_corr.items():
        print(f"{factor:15}: {value:+.4f}")

    print("\nObservation: Fuel price, CPI, unemployment, and temperature show weak linear")
    print("correlation with weekly store sales in this aggregate dataset.")

    return corr_matrix


if __name__ == "__main__":
    df = load_and_clean_data()
    analyze_correlations(df)
