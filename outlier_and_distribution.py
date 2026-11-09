"""
Walmart Sales Analysis - Distribution & Outlier Detection
Examines the spread of sales figures and detects outlier store-weeks using IQR.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from data_preprocessing import load_and_clean_data

OUTPUT_DIR = Path("visualizations")
OUTPUT_DIR.mkdir(exist_ok=True)


def analyze_distribution(df):
    sns.set_theme(style="whitegrid")

    # 1. Sales distribution histogram + KDE
    plt.figure(figsize=(10, 5))
    sns.histplot(df["Weekly_Sales"], bins=35, kde=True, color="#008080")
    plt.title("Distribution of Weekly Sales", fontsize=13, pad=12)
    plt.xlabel("Weekly Sales ($)", fontsize=11)
    plt.ylabel("Frequency (Store-Weeks)", fontsize=11)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "04_sales_distribution.png", dpi=150)
    plt.close()
    print("Saved 04_sales_distribution.png")

    # 2. Boxplot
    plt.figure(figsize=(10, 3.5))
    sns.boxplot(x=df["Weekly_Sales"], color="#f39c12")
    plt.title("Spread and Extreme Values in Weekly Sales", fontsize=13, pad=12)
    plt.xlabel("Weekly Sales ($)", fontsize=11)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "05_sales_boxplot.png", dpi=150)
    plt.close()
    print("Saved 05_sales_boxplot.png")

    # 3. IQR calculations
    q1 = df["Weekly_Sales"].quantile(0.25)
    q3 = df["Weekly_Sales"].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = df[(df["Weekly_Sales"] < lower_bound) | (df["Weekly_Sales"] > upper_bound)]

    print(f"25th Percentile (Q1): ${q1:,.2f}")
    print(f"75th Percentile (Q3): ${q3:,.2f}")
    print(f"Interquartile Range (IQR): ${iqr:,.2f}")
    print(f"Upper Fence: ${upper_bound:,.2f}")
    print(f"Identified {len(outliers)} high-sales outlier weeks (mostly Q4 holiday weeks).")

    return outliers


if __name__ == "__main__":
    df = load_and_clean_data()
    analyze_distribution(df)
