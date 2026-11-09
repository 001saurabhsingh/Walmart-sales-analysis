# Walmart Sales Analysis

An exploratory data analysis (EDA) of weekly sales data from 45 Walmart stores between February 2010 and October 2012. This project investigates seasonal patterns, holiday demand surges, store-level sales variance, and the relationship between retail revenue and macroeconomic factors.

---

## Key Findings

* **Holiday Lift:** Holiday weeks generate an average sales lift of **+7.8%** compared to non-holiday weeks. Peak surges occur in late November (Thanksgiving / Black Friday) and mid-to-late December (Christmas).
* **Monthly Seasonality:** **December** posts the highest average weekly sales (**$1,281,863**), followed by November. The lowest sales occur in January and February after holiday spending cools down.
* **Store Performance Disparities:** Store **20** achieves the highest average weekly sales (**$2,107,677**), while Store **33** averages the lowest (**$259,862**).
* **Outlier Store-Weeks:** The 1.5 &times; IQR rule flags **34 store-weeks** as high-sales outliers (sales > $2.72M). These correspond directly to Thanksgiving and Christmas retail surges rather than data errors.
* **Macroeconomic Factors:** Linear correlation between sales and external indicators is weak across the dataset (Unemployment: -0.11, CPI: -0.07, Temperature: -0.06, Fuel Price: +0.01).

---

## Project Structure & Modular Files

The analysis is organized into modular scripts and dedicated notebooks:

```text
walmart_sales_analysis/
├── data/
│   └── Walmart_Sales.csv             # Raw dataset (6,435 rows, 8 columns)
├── visualizations/                   # Generated charts & figures
│   ├── 01_top_stores.png
│   ├── 02_weekly_sales_trend.png
│   ├── 03_monthly_sales.png
│   ├── 04_sales_distribution.png
│   ├── 05_sales_boxplot.png
│   ├── 06_holiday_comparison.png
│   └── 07_correlation_heatmap.png
│
├── Notebooks:
│   ├── numpy.ipynb                   # NumPy array operations, percentiles, IQR, and masking
│   ├── matplotlib.ipynb              # Matplotlib & Seaborn visualizations (line, bar, hist, box, heatmap)
│   └── Walmart_Sales_Analysis.ipynb  # End-to-end comprehensive project analysis notebook
│
├── Python Modules:
│   ├── data_preprocessing.py         # Data loading, date parsing (DD-MM-YYYY), and feature extraction
│   ├── store_analysis.py             # Store-level performance, top/bottom rankings, and bar charts
│   ├── trend_analysis.py             # Weekly time series, monthly seasonality, and holiday comparison
│   ├── outlier_and_distribution.py   # Sales distribution plots and IQR outlier calculations
│   ├── economic_factors.py           # Correlation matrix of sales vs CPI, unemployment, fuel price
│   ├── main.py                       # Unified runner script executing the full pipeline
│   └── walmart_sales_analysis.py     # Standalone end-to-end script
│
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation
```

---

## Visualizations

| Chart | Description |
| :--- | :--- |
| ![Top Stores](visualizations/01_top_stores.png) | **Store Rankings:** Top 10 stores ranked by average weekly revenue. |
| ![Weekly Trend](visualizations/02_weekly_sales_trend.png) | **Sales Trend (2010–2012):** Combined weekly sales showing clear Q4 holiday spikes. |
| ![Monthly Sales](visualizations/03_monthly_sales.png) | **Seasonality:** Monthly averages showing peak volume in December. |
| ![Distribution](visualizations/04_sales_distribution.png) | **Distribution:** Histogram with KDE showing right-skewed sales volume. |
| ![Box Plot](visualizations/05_sales_boxplot.png) | **Outlier Detection:** Boxplot identifying high-volume holiday weeks. |
| ![Holiday Comparison](visualizations/06_holiday_comparison.png) | **Holiday vs Regular:** Comparing revenue during holiday vs regular weeks (+7.8% lift). |
| ![Correlation Heatmap](visualizations/07_correlation_heatmap.png) | **Economic Indicators:** Correlation matrix for temperature, fuel price, CPI, and unemployment. |

---

## Setup & Running the Code

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Full Analysis Pipeline
You can run the unified pipeline from terminal:
```bash
python main.py
```
Or execute any individual module directly (e.g., `python store_analysis.py`).

### 3. Open the Jupyter Notebooks
Launch Jupyter:
```bash
jupyter notebook
```
- Open `Walmart_Sales_Analysis.ipynb` for the full end-to-end exploratory analysis.
- Open `numpy.ipynb` for NumPy specific calculations (percentiles, IQR, array manipulation).
- Open `matplotlib.ipynb` for step-by-step plotting examples with Matplotlib and Seaborn.
