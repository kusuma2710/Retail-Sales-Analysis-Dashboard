from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

np.random.seed(42)

products = {
    "Electronics": [("Laptop", 800), ("Headphones", 60)],
    "Clothing": [("Shirt", 25), ("Shoes", 70)],
    "Groceries": [("Rice", 15), ("Milk", 5)]
}

rows = []

for order_id in range(1, 501):
    category = np.random.choice(list(products.keys()))

    product, price = products[category][
        np.random.randint(len(products[category]))
    ]

    date = pd.Timestamp("2025-01-01") + pd.Timedelta(
        days=int(np.random.randint(0, 365))
    )

    rows.append({
        "Order_ID": order_id,
        "Date": date,
        "Category": category,
        "Product": product,
        "Quantity": int(np.random.randint(1, 6)),
        "Unit_Price": price
    })

df = pd.DataFrame(rows)

df.to_csv(DATA_DIR / "sales_data.csv", index=False)

print("Dataset created successfully!")
print("Total transactions:", len(df))
print(df.head())