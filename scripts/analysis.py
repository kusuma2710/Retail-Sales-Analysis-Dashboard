from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(BASE_DIR / "data" / "sales_data.csv")

# Display first five rows
print("First 5 rows:")
print(df.head())

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Remove duplicates and missing values
df = df.drop_duplicates(subset="Order_ID")
df = df.dropna()

# Convert date column
df["Date"] = pd.to_datetime(df["Date"])

# Calculate revenue
df["Revenue"] = df["Quantity"] * df["Unit_Price"]

# Total revenue
print("\nTotal Revenue:", df["Revenue"].sum())

# Total orders
print("Total Orders:", df["Order_ID"].nunique())

# Average order value
print(
    "Average Order Value:",
    df["Revenue"].sum() / df["Order_ID"].nunique()
)

# Revenue by category
print("\nRevenue by Category:")
print(df.groupby("Category")["Revenue"].sum())

# Monthly revenue
df["Month"] = df["Date"].dt.to_period("M").astype(str)

monthly_sales = df.groupby("Month")["Revenue"].sum()

# Create outputs folder
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Create chart
monthly_sales.plot(
    kind="bar",
    figsize=(10, 5),
    color="steelblue",
    title="Monthly Sales Revenue"
)

plt.xlabel("Month")
plt.ylabel("Revenue ($)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(OUTPUT_DIR / "sales_chart.png")
plt.close()

print("\nChart saved successfully!")