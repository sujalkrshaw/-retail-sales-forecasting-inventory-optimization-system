import streamlit as st
import pandas as pd
from model import train_model, predict_sales

df = pd.read_csv("app/sales.csv")

st.title("📊 Retail Sales Dashboard")

# FILTER
product = st.selectbox("Select Product", df["product"].unique())
filtered_df = df[df["product"] == product]

# KPI
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", filtered_df["sales"].sum())
col2.metric("Max Sales", filtered_df["sales"].max())
col3.metric("Min Sales", filtered_df["sales"].min())

# CHART
st.write("### Sales Trend")
daily_sales = filtered_df.groupby("day")["sales"].sum()
st.line_chart(daily_sales)

# 🔥 ML PART (AFTER filtered_df is created)
model = train_model(filtered_df)

st.write("### 📈 Sales Prediction vs Actual")

# Past data
past_days = filtered_df["day"]
past_sales = filtered_df["sales"]

# Future prediction
future_days = list(range(31, 41))
predictions = predict_sales(model, future_days)

# Combine both
combined_df = pd.DataFrame({
    "day": list(past_days) + future_days,
    "sales": list(past_sales) + list(predictions)
})

# Show graph
st.line_chart(combined_df.set_index("day"))

# Show prediction table
st.write("### Prediction Values")
st.dataframe(pd.DataFrame({
    "day": future_days,
    "predicted_sales": predictions
}))