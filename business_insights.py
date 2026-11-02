import pandas as pd

df = pd.read_csv("retail_sales_clean.csv")

# Convert dates
df["sale_date"] = pd.to_datetime(df["sale_date"])

# Overall performance
revenue = df["revenue_ksh"].sum()
profit = df["profit_ksh"].sum()
margin = (profit / revenue) * 100

print("\n========== BUSINESS PERFORMANCE ==========")

print(f"Total Revenue: KSh {revenue:,.2f}")
print(f"Total Profit: KSh {profit:,.2f}")
print(f"Profit Margin: {margin:.2f}%")

# Branch performance
branches = df.groupby("branch")["revenue_ksh"].sum()

print("\n========== BRANCH PERFORMANCE ==========")
print(branches.sort_values(ascending=False).round(2))

print("\nBest-performing branch:", branches.idxmax())

# Category performance
categories = df.groupby("category").agg(
    Revenue=("revenue_ksh", "sum"),
    Profit=("profit_ksh", "sum")
)

print("\n========== CATEGORY PERFORMANCE ==========")
print(categories.sort_values(
    by="Revenue",
    ascending=False
).round(2))

print("\nTop revenue category:", categories["Revenue"].idxmax())

# Product performance
products = df.groupby("product").agg(
    Revenue=("revenue_ksh", "sum"),
    Units_Sold=("quantity", "sum")
)

print("\n========== PRODUCT PERFORMANCE ==========")
print(products.sort_values(
    by="Revenue",
    ascending=False
).head(5).round(2))

# Monthly performance
monthly = df.groupby(
    df["sale_date"].dt.month
).agg(
    Revenue=("revenue_ksh", "sum"),
    Profit=("profit_ksh", "sum")
)

monthly.index = monthly.index.map(
    lambda month: pd.Timestamp(
        year=2025,
        month=month,
        day=1
    ).strftime("%B")
)

print("\n========== MONTHLY PERFORMANCE ==========")
print(monthly.round(2))

print("\nBest sales month:", monthly["Revenue"].idxmax())

print("\n========== ANALYSIS COMPLETE ==========")