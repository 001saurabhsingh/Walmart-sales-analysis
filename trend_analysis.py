"""
Walmart Sales Analysis - Sales Trends & Seasonality
Examines time-series sales trends, monthly seasonality, and holiday spikes.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from data_preprocessing import load_and_clean_data

OUTPUT_DIR = Path("visualizations")
OUTPUT_DIR.mkdir(exist_ok=True)


def analyze_trends(df):
    sns.set_theme(style="whitegrid")

    # 1. Weekly sales trend across all 45 stores
    weekly_total = (
        df.groupby("Date", as_index=False)["Weekly_Sales"]
        .sum()
        .sort_values("Date")
    )

    plt.figure(figsize=(12, 5))
    sns.lineplot(data=weekly_total, x="Date", y="Weekly_Sales", color="#1b7837", linewidth=1.8)
    plt.title("Total Weekly Sales Trend Across All Stores (2010 - 2012)", fontsize=13, pad=12)
    plt.xlabel("Date", fontsize=11)
    plt.ylabel("Combined Sales ($)", fontsize=11)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "02_weekly_sales_trend.png", dpi=150)
    plt.close()
    print("Saved 02_weekly_sales_trend.png")

    # 2. Monthly average sales pattern
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_sales = df.groupby("Month")["Weekly_Sales"].mean().reset_index()
    monthly_sales["Month_Name"] = monthly_sales["Month"].apply(lambda m: month_names[m - 1])

    plt.figure(figsize=(10, 5))
    sns.barplot(data=monthly_sales, x="Month_Name", y="Weekly_Sales", color="#4374b3")
    plt.title("Average Weekly Sales by Month", fontsize=13, pad=12)
    plt.xlabel("Month", fontsize=11)
    plt.ylabel("Average Weekly Sales ($)", fontsize=11)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "03_monthly_sales.png", dpi=150)
    plt.close()
    print("Saved 03_monthly_sales.png")

    # 3. Holiday vs Non-Holiday comparison
    holiday_stats = df.groupby("Holiday_Flag")["Weekly_Sales"].agg(["mean", "median", "count"]).round(2)
    holiday_stats.index = ["Non-Holiday Week", "Holiday Week"]

    avg_nonholiday = holiday_stats.loc["Non-Holiday Week", "mean"]
    avg_holiday = holiday_stats.loc["Holiday Week", "mean"]
    pct_lift = ((avg_holiday - avg_nonholiday) / avg_nonholiday) * 100

    print(f"\nHoliday week avg: ${avg_holiday:,.2f} vs Non-holiday avg: ${avg_nonholiday:,.2f}")
    print(f"Holiday sales lift: +{pct_lift:.2f}%")

    plot_data = holiday_stats.reset_index(names="Week_Type")
    plt.figure(figsize=(7, 5))
    sns.barplot(data=plot_data, x="Week_Type", y="mean", color="#756bb1")
    plt.title("Holiday vs Non-Holiday Weekly Sales Comparison", fontsize=13, pad=12)
    plt.xlabel("")
    plt.ylabel("Average Weekly Sales ($)", fontsize=11)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "06_holiday_comparison.png", dpi=150)
    plt.close()
    print("Saved 06_holiday_comparison.png")

    return weekly_total, monthly_sales, holiday_stats


if __name__ == "__main__":
    df = load_and_clean_data()
    analyze_trends(df)
