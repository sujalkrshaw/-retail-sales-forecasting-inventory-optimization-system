import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression

df = pd.read_csv("data/sales.csv")

st.title("Retail Sales Forecasting & Inventory Optimization System")

# Sales trend
daily_sales = df.groupby("day")["sales"].sum()
st.line_chart(daily_sales)

# Product sales
product_sales = df.groupby("product")["sales"].sum()
st.bar_chart(product_sales)

# Forecast
df_grouped = df.groupby("day")["sales"].sum().reset_index()
X = df_grouped["day"].values.reshape(-1, 1)
y = df_grouped["sales"].values

model = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
model.fit(X, y)

future_days = list(range(6, 11))
future_array = np.array(future_days).reshape(-1, 1)
predictions = model.predict(future_array)

forecast_df = pd.DataFrame({
    "Day": future_days,
    "Predicted Sales": predictions
}).set_index("Day")

st.subheader("Sales Forecast")
st.line_chart(forecast_df)

# Inventory
avg_sales = df.groupby("product")["sales"].mean() * 1.1

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

    status = "Reorder Needed" if stock < reorder_point else "Stock OK"
    reorder_qty = round(max(0, reorder_point - stock), 2)

    inventory.append([product, avg, reorder_point, stock, reorder_qty, status])

inventory_df = pd.DataFrame(inventory, columns=["Product","Avg Sales","ROP","Stock","Reorder Qty","Status"])
st.dataframe(inventory_df)
