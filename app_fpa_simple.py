import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="FP&A Actual Spend Dashboard", layout="wide")

st.title("📊 FP&A Actual Spend Analytics")

@st.cache_data
def load_data():
    return pd.read_csv("data/fpa_actual_1000.csv", parse_dates=["Date"])

df = load_data()

df["Month"] = df["Date"].dt.to_period("M").astype(str)

# Sidebar filters
st.sidebar.header("Filters")

entity = st.sidebar.multiselect("Entity", df["Company_Entity"].unique(), default=df["Company_Entity"].unique())
country = st.sidebar.multiselect("Country", df["Country"].unique(), default=df["Country"].unique())
function = st.sidebar.multiselect("Function", df["Function"].unique(), default=df["Function"].unique())

filtered_df = df[
    (df["Company_Entity"].isin(entity)) &
    (df["Country"].isin(country)) &
    (df["Function"].isin(function))
]

# KPI
st.subheader("Executive Snapshot")

col1, col2, col3 = st.columns(3)

col1.metric("Total Spend", f"${filtered_df['Actual_Amount_USD'].sum():,.0f}")
col2.metric("Total POs", len(filtered_df))
col3.metric("Avg PO Value", f"${filtered_df['Actual_Amount_USD'].mean():,.0f}")

# Monthly trend
st.subheader("Monthly Spend Trend")

monthly = filtered_df.groupby("Month")["Actual_Amount_USD"].sum().reset_index()

fig_month = px.line(monthly, x="Month", y="Actual_Amount_USD", markers=True)
st.plotly_chart(fig_month, use_container_width=True)

# Vendor concentration
st.subheader("Top 10 Vendors")

vendor_spend = (
    filtered_df.groupby("Vendor")["Actual_Amount_USD"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_vendor = px.bar(vendor_spend, x="Vendor", y="Actual_Amount_USD")
st.plotly_chart(fig_vendor, use_container_width=True)

# GL concentration
st.subheader("GL Spend Concentration")

gl_spend = (
    filtered_df.groupby("GL_Code")["Actual_Amount_USD"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig_gl = px.bar(gl_spend, x="GL_Code", y="Actual_Amount_USD")
st.plotly_chart(fig_gl, use_container_width=True)

# Dynamic drilldown
st.subheader("Dynamic Drilldown")

dimensions = [
    "Vendor",
    "Country",
    "Cost_Center",
    "Profit_Center",
    "Function",
    "GL_Code",
    "Expense_Head",
    "PO_Number"
]

selected_dims = st.multiselect("Select Dimensions", dimensions, default=["Vendor"])

if selected_dims:
    dynamic = (
        filtered_df.groupby(selected_dims)["Actual_Amount_USD"]
        .sum()
        .reset_index()
        .sort_values("Actual_Amount_USD", ascending=False)
    )

    st.dataframe(dynamic)

st.caption("FP&A Actual Spend Dashboard | No Budget Version")