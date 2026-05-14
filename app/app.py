import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Retail Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.main {
    background-color: #0f172a;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

h1, h2, h3 {
    color: white;
}

.stMetric {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}

div[data-testid="metric-container"] {
    background-color: #1e293b;
    border: 1px solid #334155;
    padding: 15px;
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙ Dashboard Controls")

selected_product = st.sidebar.selectbox(
    "Select Product",
    ["All", "Bread", "Chips", "Cola", "Milk", "Soap"]
)

forecast_days = st.sidebar.slider(
    "Forecast Days",
    7,
    30,
    7
)

# ---------------- TITLE ----------------
st.title("🛒 AI Retail Sales & Inventory Dashboard")

st.markdown("""
### 🚀 Smart Retail Analytics, Demand Forecasting & Inventory Optimization System
""")

# ---------------- SAMPLE DATA ----------------
days = list(range(1, 31))

sales = [
    300, 305, 280, 375, 210,
    320, 382, 290, 185, 220,
    245, 272, 420, 283, 302,
    244, 303, 328, 299, 318,
    238, 374, 287, 249, 345,
    315, 266, 243, 218, 290
]

df = pd.DataFrame({
    "Day": days,
    "Sales": sales
})

# ---------------- KPI SECTION ----------------
st.markdown("## 📌 Business KPIs")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Revenue",
    "₹8,664",
    "+12%"
)

col2.metric(
    "📈 Avg Daily Sales",
    "₹288",
    "+5%"
)

col3.metric(
    "📦 Products To Reorder",
    "4",
    "-2"
)

col4.metric(
    "🔥 Highest Sale",
    "₹420",
    "+18%"
)

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Sales Analytics",
    "🔮 Forecasting",
    "📦 Inventory",
    "📊 Insights"
])

# ==================================================
# TAB 1
# ==================================================
with tab1:

    st.subheader("📈 Daily Sales Trend")

    fig = px.line(
        df,
        x="Day",
        y="Sales",
        markers=True,
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("📊 Product-wise Sales")

    product_df = pd.DataFrame({
        "Product": ["Bread", "Chips", "Cola", "Milk", "Soap"],
        "Sales": [1830, 1580, 1890, 1835, 1560]
    })

    fig2 = px.bar(
        product_df,
        x="Product",
        y="Sales",
        text="Sales",
        template="plotly_dark"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ==================================================
# TAB 2
# ==================================================
with tab2:

    st.subheader("🔮 AI Sales Forecast")

    future_x = list(range(31, 31 + forecast_days))

    future_sales = np.linspace(
        260,
        240,
        forecast_days
    )

    forecast_df = pd.DataFrame({
        "Day": future_x,
        "Forecast Sales": future_sales
    })

    fig3 = go.Figure()

    fig3.add_trace(go.Scatter(
        x=df["Day"],
        y=df["Sales"],
        mode='lines+markers',
        name='Historical Sales'
    ))

    fig3.add_trace(go.Scatter(
        x=forecast_df["Day"],
        y=forecast_df["Forecast Sales"],
        mode='lines+markers',
        name='Forecast'
    ))

    fig3.update_layout(
        template="plotly_dark",
        title="Sales Forecast"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    st.dataframe(forecast_df)

# ==================================================
# TAB 3
# ==================================================
with tab3:

    st.subheader("📦 Inventory Optimization")

    inventory_df = pd.DataFrame({

        "Product": [
            "Bread",
            "Chips",
            "Cola",
            "Milk",
            "Soap"
        ],

        "Avg Sales": [
            67.03,
            57.60,
            69.15,
            67.06,
            56.83
        ],

        "Reorder Point": [
            355.15,
            308.00,
            365.75,
            355.30,
            304.15
        ],

        "Current Stock": [
            250,
            300,
            150,
            200,
            400
        ]
    })

    inventory_df["Reorder Qty"] = (
        inventory_df["Reorder Point"]
        - inventory_df["Current Stock"]
    ).clip(lower=0)

    inventory_df["Status"] = inventory_df[
        "Reorder Qty"
    ].apply(
        lambda x:
        "⚠ Reorder Needed"
        if x > 0
        else "✅ Stock OK"
    )

    st.dataframe(
        inventory_df,
        use_container_width=True
    )

    st.error(
        "⚠ Urgent: Reorder required for Bread, Chips, Cola and Milk"
    )

# ==================================================
# TAB 4
# ==================================================
with tab4:

    st.subheader("📊 Business Insights")

    st.info("""
    📈 Sales increased by 12% this month.

    📦 Cola is the top-selling product.

    ⚠ Bread inventory is critically low.

    🚀 Forecast indicates stable future demand.
    """)

    pie_fig = px.pie(
        product_df,
        names="Product",
        values="Sales",
        hole=0.5,
        template="plotly_dark"
    )

    st.plotly_chart(
        pie_fig,
        use_container_width=True
    )

# ---------------- DOWNLOAD BUTTON ----------------
st.download_button(
    label="📥 Download Sales Report",
    data=df.to_csv(index=False),
    file_name="sales_report.csv",
    mime="text/csv"
)

# ---------------- FOOTER ----------------
st.markdown("---")

st.markdown("""
<center>

## 🤖 AI-Powered Retail Forecasting System

Built using Python, Streamlit, Plotly & Machine Learning

</center>
""", unsafe_allow_html=True)