"""
Walmart Sales Analysis
Exploratory data analysis of weekly store sales across 45 Walmart branches.
Analyzes sales trends, seasonality, holiday impacts, and economic correlations.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Styling configuration
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 5)

DATA_PATH = Path("data/Walmart_Sales.csv")
OUTPUT_DIR = Path("visualizations")
OUTPUT_DIR.mkdir(exist_ok=True)


def main():
    # ---------------------------------------------------------
    # 1. Load Data & Basic Exploration
    # ---------------------------------------------------------
    df = pd.read_csv(DATA_PATH)
    print(f"Loaded {df.shape[0]:,} rows and {df.shape[1]} columns.")
    print("\nSample records:")
    print(df.head())

    # Data quality check
    print("\nMissing values:")
    print(df.isnull().sum())
    print(f"Duplicate rows: {df.duplicated().sum()}")

    # ---------------------------------------------------------
    # 2. Date Formatting & Feature Extraction
    # ---------------------------------------------------------
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Week"] = df["Date"].dt.isocalendar().week.astype("int64")

    # Overall metrics
    total_sales = df["Weekly_Sales"].sum()
    avg_sales = df["Weekly_Sales"].mean()
    median_sales = df["Weekly_Sales"].median()
    start_date = df["Date"].min().strftime("%d-%b-%Y")
    end_date = df["Date"].max().strftime("%d-%b-%Y")

    print("\n--- Sales Overview ---")
    print(f"Total Sales:        ${total_sales:,.2f}")
    print(f"Average Weekly:     ${avg_sales:,.2f}")
    print(f"Median Weekly:      ${median_sales:,.2f}")
    print(f"Reporting Period:   {start_date} to {end_date} (45 stores)")

    # ---------------------------------------------------------
    # 3. Store Performance Comparison
    # ---------------------------------------------------------
    store_perf = (
        df.groupby("Store")["Weekly_Sales"]
        .agg(Total_Sales="sum", Avg_Weekly_Sales="mean", Weeks_Recorded="count")
        .sort_values("Avg_Weekly_Sales", ascending=False)
    )

    top_10 = store_perf.head(10).reset_index()
    print("\nTop 5 Performing Stores (Avg Weekly Sales):")
    print(top_10.head(5).round(2))

    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_10, x="Avg_Weekly_Sales", y="Store", orient="h", color="steelblue")
    plt.title("Top 10 Stores by Average Weekly Sales")
    plt.xlabel("Average Weekly Sales ($)")
    plt.ylabel("Store Number")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "01_top_stores.png", dpi=150)
    plt.close()

    # ---------------------------------------------------------
    # 4. Weekly Sales Trend
    # ---------------------------------------------------------
    weekly_trend = df.groupby("Date", as_index=False)["Weekly_Sales"].sum()

    plt.figure(figsize=(12, 5))
    sns.lineplot(data=weekly_trend, x="Date", y="Weekly_Sales", color="darkgreen", linewidth=1.5)
    plt.title("Total Weekly Sales Trend Across All Stores (2010 - 2012)")
    plt.xlabel("Date")
    plt.ylabel("Total Sales ($)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "02_weekly_sales_trend.png", dpi=150)
    plt.close()

    # ---------------------------------------------------------
    # 5. Monthly Seasonality
    # ---------------------------------------------------------
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_sales = df.groupby("Month")["Weekly_Sales"].mean().reset_index()
    monthly_sales["Month_Name"] = monthly_sales["Month"].apply(lambda m: month_names[m - 1])

    plt.figure(figsize=(10, 5))
    sns.barplot(data=monthly_sales, x="Month_Name", y="Weekly_Sales", color="cornflowerblue")
    plt.title("Average Weekly Sales by Month")
    plt.xlabel("Month")
    plt.ylabel("Average Weekly Sales ($)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "03_monthly_sales.png", dpi=150)
    plt.close()

    # ---------------------------------------------------------
    # 6. Sales Spread & Outlier Detection
    # ---------------------------------------------------------
    plt.figure(figsize=(10, 5))
    sns.histplot(df["Weekly_Sales"], bins=35, kde=True, color="teal")
    plt.title("Distribution of Weekly Sales")
    plt.xlabel("Weekly Sales ($)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "04_sales_distribution.png", dpi=150)
    plt.close()

    plt.figure(figsize=(10, 3.5))
    sns.boxplot(x=df["Weekly_Sales"], color="orange")
    plt.title("Spread and Outliers in Weekly Sales")
    plt.xlabel("Weekly Sales ($)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "05_sales_boxplot.png", dpi=150)
    plt.close()

    # IQR calculation
    q1 = df["Weekly_Sales"].quantile(0.25)
    q3 = df["Weekly_Sales"].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = df[(df["Weekly_Sales"] < lower_bound) | (df["Weekly_Sales"] > upper_bound)]

    print(f"\n25th Percentile: ${q1:,.2f}")
    print(f"75th Percentile: ${q3:,.2f}")
    print(f"IQR:             ${iqr:,.2f}")
    print(f"Flagged {len(outliers)} store-weeks exceeding upper IQR threshold (${upper_bound:,.2f})")

    # ---------------------------------------------------------
    # 7. Holiday vs Non-Holiday Performance
    # ---------------------------------------------------------
    holiday_summary = (
        df.groupby("Holiday_Flag")["Weekly_Sales"]
        .agg(["mean", "median", "count"])
    )
    holiday_summary.index = ["Non-Holiday Weeks", "Holiday Weeks"]

    h_avg = holiday_summary.loc["Holiday Weeks", "mean"]
    nh_avg = holiday_summary.loc["Non-Holiday Weeks", "mean"]
    lift = ((h_avg - nh_avg) / nh_avg) * 100

    print(f"\nHoliday Avg: ${h_avg:,.2f} vs Non-Holiday Avg: ${nh_avg:,.2f}")
    print(f"Holiday Sales Lift: +{lift:.2f}%")

    plot_holiday = holiday_summary.reset_index(names="Week_Type")
    plt.figure(figsize=(7, 5))
    sns.barplot(data=plot_holiday, x="Week_Type", y="mean", color="mediumpurple")
    plt.title("Average Sales: Holiday vs Regular Weeks")
    plt.xlabel("")
    plt.ylabel("Average Weekly Sales ($)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "06_holiday_comparison.png", dpi=150)
    plt.close()

    # ---------------------------------------------------------
    # 8. External Factors & Correlation Heatmap
    # ---------------------------------------------------------
    numeric_df = df.select_dtypes(include="number")
    corr = numeric_df.corr()

    plt.figure(figsize=(9, 7))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0)
    plt.title("Correlation Matrix: Sales vs External Factors")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "07_correlation_heatmap.png", dpi=150)
    plt.close()

    ext_factors = ["Temperature", "Fuel_Price", "CPI", "Unemployment"]
    print("\nCorrelation with Weekly Sales:")
    print(corr["Weekly_Sales"][ext_factors].sort_values().to_frame("Correlation"))

    # Save processed dataset
    df.to_csv("cleaned_walmart_sales.csv", index=False)
    print("\nCleaned data exported to cleaned_walmart_sales.csv")


if __name__ == "__main__":
    main()
