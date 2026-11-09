"""
Walmart Sales Analysis - Store Performance
Compares weekly sales performance across the 45 Walmart stores.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from data_preprocessing import load_and_clean_data

OUTPUT_DIR = Path("visualizations")
OUTPUT_DIR.mkdir(exist_ok=True)


def analyze_store_sales(df):
    # Store sales aggregation
    store_stats = (
        df.groupby("Store")["Weekly_Sales"]
        .agg(
            Total_Sales="sum",
            Avg_Weekly_Sales="mean",
            Std_Weekly_Sales="std",
            Weeks_Count="count"
        )
        .sort_values(by="Avg_Weekly_Sales", ascending=False)
    )

    top_10 = store_stats.head(10).reset_index()
    bottom_5 = store_stats.tail(5).reset_index()

    print("--- Top 5 Highest Performing Stores (by Avg Weekly Sales) ---")
    for _, row in top_10.head(5).iterrows():
        print(f"Store {int(row['Store'])}: ${row['Avg_Weekly_Sales']:,.2f} / week (Total: ${row['Total_Sales']:,.2f})")

    print("\n--- Bottom 5 Stores ---")
    for _, row in bottom_5.iterrows():
        print(f"Store {int(row['Store'])}: ${row['Avg_Weekly_Sales']:,.2f} / week")

    # Plot top 10 stores
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")
    sns.barplot(data=top_10, x="Avg_Weekly_Sales", y="Store", orient="h", color="#2b5c8f")
    plt.title("Top 10 Walmart Stores by Average Weekly Sales", fontsize=14, pad=12)
    plt.xlabel("Average Weekly Sales ($)", fontsize=11)
    plt.ylabel("Store Number", fontsize=11)
    plt.tight_layout()

    out_path = OUTPUT_DIR / "01_top_stores.png"
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved chart to {out_path}")

    return store_stats


if __name__ == "__main__":
    df = load_and_clean_data()
    analyze_store_sales(df)
