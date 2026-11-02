import pandas as pd

# Load cleaned data
df = pd.read_csv("retail_sales_clean.csv")

# Convert date column
df["sale_date"] = pd.to_datetime(df["sale_date"])

# Create summary figures
total_revenue = df["revenue_ksh"].sum()
total_profit = df["profit_ksh"].sum()
total_transactions = len(df)
total_units = df["quantity"].sum()

profit_margin = (total_profit / total_revenue) * 100

# Overall sales summary
summary = pd.DataFrame({
    "Business Metric": [
        "Total Revenue (KSh)",
        "Total Profit (KSh)",
        "Total Transactions",
        "Units Sold",
        "Profit Margin (%)"
    ],
    "Value": [
        total_revenue,
        total_profit,
        total_transactions,
        total_units,
        round(profit_margin, 2)
    ]
})

# Branch performance
branch_summary = df.groupby("branch").agg(
    Revenue=("revenue_ksh", "sum"),
    Profit=("profit_ksh", "sum"),
    Transactions=("transaction_id", "count"),
    Units_Sold=("quantity", "sum")
).reset_index()

# Category performance
category_summary = df.groupby("category").agg(
    Revenue=("revenue_ksh", "sum"),
    Profit=("profit_ksh", "sum")
).reset_index()

# Monthly performance
monthly_summary = df.groupby(
    ["year", "month", "month_name"]
).agg(
    Revenue=("revenue_ksh", "sum"),
    Profit=("profit_ksh", "sum")
).reset_index()

# Export everything to Excel
with pd.ExcelWriter(
    "retail_sales_report.xlsx",
    engine="openpyxl"
) as writer:

    df.to_excel(
        writer,
        sheet_name="Cleaned Data",
        index=False
    )

    summary.to_excel(
        writer,
        sheet_name="Sales Summary",
        index=False
    )

    branch_summary.to_excel(
        writer,
        sheet_name="Branch Analysis",
        index=False
    )

    category_summary.to_excel(
        writer,
        sheet_name="Category Analysis",
        index=False
    )

    monthly_summary.to_excel(
        writer,
        sheet_name="Monthly Analysis",
        index=False
    )

print("Excel report created successfully!")
print("File: retail_sales_report.xlsx")