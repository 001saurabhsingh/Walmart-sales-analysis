"""
Walmart Sales Analysis - Main Pipeline Runner
Executes the modular data cleaning, store ranking, trend, outlier, and correlation analyses.
"""

from data_preprocessing import load_and_clean_data
from store_analysis import analyze_store_sales
from trend_analysis import analyze_trends
from outlier_and_distribution import analyze_distribution
from economic_factors import analyze_correlations


def run_full_pipeline():
    print("=" * 60)
    print("WALMART SALES ANALYSIS - END-TO-END PIPELINE")
    print("=" * 60)

    # 1. Load and prepare dataset
    print("\n[Step 1] Loading and cleaning data...")
    df = load_and_clean_data()

    # 2. Store performance
    print("\n[Step 2] Evaluating store-level sales performance...")
    analyze_store_sales(df)

    # 3. Trends and seasonality
    print("\n[Step 3] Analyzing weekly trends and monthly seasonality...")
    analyze_trends(df)

    # 4. Distribution and outliers
    print("\n[Step 4] Checking sales distribution and IQR outliers...")
    analyze_distribution(df)

    # 5. Economic factors correlation
    print("\n[Step 5] Checking correlation with macroeconomic variables...")
    analyze_correlations(df)

    print("\n" + "=" * 60)
    print("Pipeline completed successfully! All charts saved to 'visualizations/'")
    print("=" * 60)


if __name__ == "__main__":
    run_full_pipeline()
