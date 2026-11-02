import pandas as pd

# Load the raw dataset
df = pd.read_csv("retail_sales_raw.csv")

print("INITIAL DATASET")
print("Total records:", len(df))
print("Duplicate transactions:", df.duplicated(subset="transaction_id").sum())

print("\nMissing values:")
print(df.isnull().sum())


# 1. Remove duplicate transactions
df = df.drop_duplicates(subset="transaction_id")


# 2. Clean product names
df["product"] = (
    df["product"]
    .astype(str)
    .str.strip()
    .str.title()
)

# Standardise product names
product_mapping = {
    "Sugar 2Kg": "Sugar 2kg",
    "Cooking Oil 1L": "Cooking Oil 1L",
    "Rice 5Kg": "Rice 5kg",
    "Maize Flour 2Kg": "Maize Flour 2kg",
    "Milk 500Ml": "Milk 500ml",
    "Bluetooth Speaker": "Bluetooth Speaker",
    "Earphones": "Earphones",
    "Phone Charger": "Phone Charger",
    "Men'S Shirt": "Men's Shirt",
    "Women'S Dress": "Women's Dress",
    "Bedsheet": "Bedsheet",
    "Cooking Pot": "Cooking Pot"
}

df["product"] = df["product"].replace(product_mapping)


# 3. Clean category names
df["category"] = (
    df["category"]
    .astype(str)
    .str.strip()
    .str.title()
)


# 4. Clean branch names
df["branch"] = (
    df["branch"]
    .astype(str)
    .str.strip()
    .str.title()
)


# 5. Convert dates
df["sale_date"] = pd.to_datetime(
    df["sale_date"],
    format="mixed",
    dayfirst=True,
    errors="coerce"
)

# Remove rows with invalid dates
df = df.dropna(subset=["sale_date"])


# 6. Convert numerical columns
numeric_columns = [
    "quantity",
    "unit_price_ksh",
    "unit_cost_ksh",
    "discount_pct"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")


# 7. Handle missing values
df["payment_method"] = df["payment_method"].fillna("Unknown")

# Remove records without essential numerical values
df = df.dropna(subset=[
    "quantity",
    "unit_price_ksh",
    "unit_cost_ksh",
    "discount_pct"
])


# 8. Remove invalid values
df = df[
    (df["quantity"] > 0) &
    (df["unit_price_ksh"] >= 0) &
    (df["unit_cost_ksh"] >= 0) &
    (df["discount_pct"].between(0, 100))
].copy()


# 9. Calculate sales and profit
df["gross_sales_ksh"] = (
    df["quantity"] * df["unit_price_ksh"]
)

df["discount_ksh"] = (
    df["gross_sales_ksh"] * df["discount_pct"] / 100
)

df["revenue_ksh"] = (
    df["gross_sales_ksh"] - df["discount_ksh"]
)

df["total_cost_ksh"] = (
    df["quantity"] * df["unit_cost_ksh"]
)

df["profit_ksh"] = (
    df["revenue_ksh"] - df["total_cost_ksh"]
)


# 10. Add reporting columns
df["year"] = df["sale_date"].dt.year
df["month"] = df["sale_date"].dt.month
df["month_name"] = df["sale_date"].dt.strftime("%B")


# 11. Save cleaned dataset
df.to_csv("retail_sales_clean.csv", index=False)


# 12. Display final results
print("\nCLEANING COMPLETE")
print("Remaining records:", len(df))
print("Total revenue: KSh", round(df["revenue_ksh"].sum(), 2))
print("Total profit: KSh", round(df["profit_ksh"].sum(), 2))
print("\nCleaned dataset saved as retail_sales_clean.csv")