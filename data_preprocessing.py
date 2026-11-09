"""
Walmart Sales Analysis - Data Preprocessing
Handles loading, date formatting, missing value checks, and feature extraction.
"""

from pathlib import Path
import pandas as pd


def load_and_clean_data(data_path="data/Walmart_Sales.csv"):
    path = Path(data_path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at {data_path}")

    # Load dataset
    df = pd.read_csv(path)
    print(f"Loaded dataset with {df.shape[0]:,} rows and {df.shape[1]} columns.")

    # Check for missing values & duplicate records
    missing = df.isnull().sum().sum()
    duplicates = df.duplicated().sum()
    print(f"Missing values: {missing} | Duplicate rows: {duplicates}")

    # Parse date column (DD-MM-YYYY format)
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")

    # Extract calendar features for seasonal analysis
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Week"] = df["Date"].dt.isocalendar().week.astype("int64")

    # Date range info
    start_date = df["Date"].min().strftime("%d-%b-%Y")
    end_date = df["Date"].max().strftime("%d-%b-%Y")
    print(f"Date range covered: {start_date} to {end_date} (45 stores)")

    return df


if __name__ == "__main__":
    df = load_and_clean_data()
    print("\nSample preview:")
    print(df.head())
