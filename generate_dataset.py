
import csv
import random
from datetime import date, timedelta

random.seed(42)

products = [
    ("Sugar 2kg", "Groceries", 320, 270),
    ("Cooking Oil 1L", "Groceries", 280, 230),
    ("Rice 5kg", "Groceries", 850, 700),
    ("Maize Flour 2kg", "Groceries", 160, 130),
    ("Milk 500ml", "Groceries", 70, 55),
    ("Bluetooth Speaker", "Electronics", 1800, 1250),
    ("Earphones", "Electronics", 650, 400),
    ("Phone Charger", "Electronics", 500, 300),
    ("Men's Shirt", "Clothing", 1200, 750),
    ("Women's Dress", "Clothing", 1800, 1100),
    ("Bedsheet", "Household", 1500, 950),
    ("Cooking Pot", "Household", 2200, 1500),
]

branches = ["Nairobi", "Thika", "Meru"]
payment_methods = ["Cash", "M-Pesa", "Card"]

start_date = date(2025, 1, 1)
end_date = date(2025, 12, 31)

days = (end_date - start_date).days

records = []

for i in range(1, 501):

    sale_date = start_date + timedelta(
        days=random.randint(0, days)
    )

    product, category, price, cost = random.choice(products)

    quantity = random.randint(1, 10)
    discount = random.choice([0, 0, 0, 5, 10, 15])

    record = {
        "transaction_id": f"TXN{i:04d}",
        "sale_date": sale_date.isoformat(),
        "branch": random.choice(branches),
        "product": product,
        "category": category,
        "quantity": quantity,
        "unit_price_ksh": price,
        "unit_cost_ksh": cost,
        "discount_pct": discount,
        "payment_method": random.choice(payment_methods)
    }

    records.append(record)


# Introduce a few deliberate data-quality issues.

# Inconsistent product names
records[10]["product"] = "  sugar 2kg "
records[25]["product"] = "COOKING OIL 1L"

# Inconsistent category formatting
records[35]["category"] = "groceries "
records[50]["category"] = "ELECTRONICS"

# Missing payment methods
records[60]["payment_method"] = ""
records[90]["payment_method"] = ""

# Missing quantities
records[100]["quantity"] = ""
records[150]["quantity"] = ""

# Inconsistent date format
records[75]["sale_date"] = "15/03/2025"

# Duplicate transactions
records.extend([
    records[20].copy(),
    records[40].copy(),
    records[80].copy()
])


filename = "retail_sales_raw.csv"

with open(filename, "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=records[0].keys()
    )

    writer.writeheader()
    writer.writerows(records)

print("Dataset created successfully!")
print(f"Total records: {len(records)}")
print(f"Saved as: {filename}")
