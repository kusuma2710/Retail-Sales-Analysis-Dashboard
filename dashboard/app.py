from pathlib import Path
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent

st.set_page_config(
    page_title="Retail Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Retail Sales Analysis Dashboard")
st.write("Sales Performance and Business Insights")

# Load dataset
df = pd.read_csv(BASE_DIR / "data" / "sales_data.csv")

# Clean data
df = df.drop_duplicates(subset="Order_ID").dropna()
df["Date"] = pd.to_datetime(df["Date"])
df["Revenue"] = df["Quantity"] * df["Unit_Price"]
df["Month"] = df["Date"].dt.to_period("M").astype(str)

# Sidebar filter
st.sidebar.header("Filters")

categories = st.sidebar.multiselect(
    "Select Product Categories",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

filtered_df = df[df["Category"].isin(categories)]

# Calculate KPIs
total_revenue = filtered_df["Revenue"].sum()
total_orders = filtered_df["Order_ID"].nunique()

average_order = (
    total_revenue / total_orders if total_orders > 0 else 0
)

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Orders", total_orders)
col3.metric("Average Order Value", f"${average_order:,.2f}")

if filtered_df.empty:
    st.warning("Please select at least one category.")
    st.stop()

# Monthly sales chart
st.subheader("Monthly Sales Revenue")
monthly_sales = filtered_df.groupby("Month")["Revenue"].sum()
st.line_chart(monthly_sales)

# Category revenue
st.subheader("Revenue by Category")
category_sales = filtered_df.groupby("Category")["Revenue"].sum()
st.bar_chart(category_sales)

# Top products
st.subheader("Top Products by Revenue")
product_sales = (
    filtered_df.groupby("Product")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)
st.bar_chart(product_sales)

# Sales data table
st.subheader("Sales Transactions")
st.dataframe(filtered_df, use_container_width=True)