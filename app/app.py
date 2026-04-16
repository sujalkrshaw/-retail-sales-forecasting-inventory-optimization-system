import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# ---------------- LOAD DATA ----------------
df = pd.read_csv("app/sales.csv")

st.title("📊 Retail Sales & Inventory Dashboard")
st.write("This dashboard analyzes sales trends and provides inventory recommendations.")

# ---------------- SALES SECTION ----------------
st.write("### 📈 Daily Sales Trend")
daily_sales = df.groupby("day")["sales"].sum()
st.line_chart(daily_sales)

st.write("### 📊 Product-wise Sales")
product_sales = df.groupby("product")["sales"].sum()
st.bar_chart(product_sales)

# ---------------- FORECAST SECTION ----------------
df_grouped = df.groupby("day")["sales"].sum().reset_index()

X = df_grouped["day"].values.reshape(-1, 1)
y = df_grouped["sales"].values

from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

model = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
model.fit(X, y)


future_days = list(range(31, 38))
future_array = np.array(future_days).reshape(-1, 1)
predictions = model.predict(future_array)

forecast_df = pd.DataFrame({
    "Day": future_days,
    "Predicted Sales": predictions
})

forecast_df.set_index("Day", inplace=True)

st.write("### 🔮 Sales Forecast (Next 7 Days)")
st.line_chart(forecast_df)

# ---------------- TOTAL SALES ----------------
st.write("### 📦 Total Sales")
st.success(int(df["sales"].sum()))

# ---------------- INVENTORY SECTION ----------------
st.write("## 📦 Inventory Status")

# Average sales + forecast adjustment
avg_sales = df.groupby("product")["sales"].mean()
forecast_factor = 1.1
avg_sales = avg_sales * forecast_factor

lead_time = 5
safety_stock = 20

current_stock = {
    "Milk": 200,
    "Chips": 300,
    "Bread": 250,
    "Soap": 400,
    "Cola": 150
}

inventory = []

for product in avg_sales.index:
    avg = round(avg_sales[product], 2)
    reorder_point = round((avg * lead_time) + safety_stock, 2)
    stock = current_stock[product]

    if stock < reorder_point:
        status = "⚠️ Reorder Needed"
    else:
        status = "✅ Stock OK"

    reorder_qty = round(max(0, reorder_point - stock), 2)

    inventory.append([
        product,
        avg,
        reorder_point,
        stock,
        reorder_qty,
        status
    ])

# ---------------- CREATE DATAFRAME ----------------
inventory_df = pd.DataFrame(
    inventory,
    columns=["Product", "Avg Sales", "Reorder Point", "Current Stock", "Reorder Qty", "Status"]
)

# ---------------- ALERT SYSTEM ----------------
low_stock = [
    p for p, s in zip(inventory_df["Product"], inventory_df["Status"])
    if "Reorder" in s
]

# ---------------- KPI CARDS ----------------
col1, col2 = st.columns(2)
col1.metric("📦 Total Sales", int(df["sales"].sum()))
col2.metric("⚠️ Products to Reorder", len(low_stock))

# ---------------- ALERT MESSAGE ----------------
if low_stock:
    st.error(f"⚠️ Urgent: Reorder required for {', '.join(low_stock)}")
else:
    st.success("✅ All products have sufficient stock")

# ---------------- HIGHLIGHT FUNCTION ----------------
def highlight_status(val):
    if "Reorder" in val:
        return "background-color: #ffcccc"
    else:
        return "background-color: #ccffcc"

# ---------------- DISPLAY TABLE ----------------
st.dataframe(inventory_df.style.map(highlight_status, subset=["Status"]))