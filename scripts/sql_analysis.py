from pathlib import Path
import pandas as pd
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent

# Load the sales dataset
df = pd.read_csv(BASE_DIR / "data" / "sales_data.csv")

# Create SQLite database in memory
conn = sqlite3.connect(":memory:")

# Convert CSV into SQL table
df.to_sql("sales", conn, if_exists="replace", index=False)

# Query 1: Revenue by Category
query1 = """
SELECT
    Category,
    SUM(Quantity * Unit_Price) AS Total_Revenue
FROM sales
GROUP BY Category
ORDER BY Total_Revenue DESC;
"""

print("\nRevenue by Category:")
print(pd.read_sql_query(query1, conn))

# Query 2: Top Products
query2 = """
SELECT
    Product,
    SUM(Quantity) AS Units_Sold,
    SUM(Quantity * Unit_Price) AS Total_Revenue
FROM sales
GROUP BY Product
ORDER BY Total_Revenue DESC;
"""

print("\nTop Selling Products:")
print(pd.read_sql_query(query2, conn))

# Query 3: Total Orders
query3 = """
SELECT
    COUNT(DISTINCT Order_ID) AS Total_Orders
FROM sales;
"""

print("\nTotal Orders:")
print(pd.read_sql_query(query3, conn))

conn.close()

print("\nSQL Analysis Completed Successfully!")