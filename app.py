import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="RetailPulse Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 RetailPulse – AI-Powered Customer Analytics & Demand Forecasting")
st.markdown("### Interactive Retail Analytics Dashboard")

# -----------------------------
# Load Dataset
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel(
        "data/online_retail_II.xlsx",
        sheet_name="Year 2010-2011"
    )

    # Remove missing Customer IDs
    df = df.dropna(subset=["Customer ID"])

    # Remove cancelled invoices
    df = df[~df["Invoice"].astype(str).str.startswith("C")]

    # Convert date
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    # Revenue column
    df["Revenue"] = df["Quantity"] * df["Price"]

    return df

df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

countries = st.sidebar.multiselect(
    "Select Country",
    sorted(df["Country"].unique()),
    default=sorted(df["Country"].unique())
)

df = df[df["Country"].isin(countries)]

# Date filter
start_date = df["InvoiceDate"].min().date()
end_date = df["InvoiceDate"].max().date()

date_range = st.sidebar.date_input(
    "Invoice Date",
    [start_date, end_date]
)

if len(date_range) == 2:
    start, end = date_range
    df = df[
        (df["InvoiceDate"].dt.date >= start) &
        (df["InvoiceDate"].dt.date <= end)
    ]

# -----------------------------
# KPIs
# -----------------------------
st.subheader("📈 Business Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Revenue",
    f"${df['Revenue'].sum():,.2f}"
)

col2.metric(
    "🛒 Total Orders",
    df["Invoice"].nunique()
)

col3.metric(
    "👥 Customers",
    df["Customer ID"].nunique()
)

col4.metric(
    "📦 Products",
    df["StockCode"].nunique()
)

st.markdown("---")

st.subheader("Dataset Preview")
st.dataframe(df.head())
...
st.subheader("Dataset Preview")
st.dataframe(df.head())

# ===========================================
# PASTE NEW CODE BELOW THIS LINE
# ===========================================

st.markdown("---")

st.subheader("📊 Analytics Dashboard")

monthly_sales = (
    df.groupby(df["InvoiceDate"].dt.to_period("M"))["Revenue"]
    .sum()
    .reset_index()
)

monthly_sales["InvoiceDate"] = monthly_sales["InvoiceDate"].astype(str)

fig1 = px.line(
    monthly_sales,
    x="InvoiceDate",
    y="Revenue",
    title="Monthly Revenue Trend",
    markers=True,
)

st.plotly_chart(fig1, use_container_width=True)

country_sales = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig2 = px.bar(
    country_sales,
    x="Country",
    y="Revenue",
    color="Revenue",
    title="Top 10 Countries by Revenue"
)

st.plotly_chart(fig2, use_container_width=True)

top_products = (
    df.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig3 = px.bar(
    top_products,
    x="Revenue",
    y="Description",
    orientation="h",
    title="Top 10 Products"
)

st.plotly_chart(fig3, use_container_width=True)

top_customers = (
    df.groupby("Customer ID")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig4 = px.bar(
    top_customers,
    x="Customer ID",
    y="Revenue",
    title="Top 10 Customers"
)

st.plotly_chart(fig4, use_container_width=True)

fig5 = px.pie(
    country_sales,
    values="Revenue",
    names="Country",
    title="Revenue Distribution by Country"
)

st.plotly_chart(fig5, use_container_width=True)