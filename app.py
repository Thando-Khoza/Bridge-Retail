
import sqlite3
import pandas as pd
import streamlit as st
from pathlib import Path


# ==================================
# PAGE CONFIGURATION
# ==================================

st.set_page_config(
    page_title="BRIDGE | Business Intelligence",
    page_icon="📊",
    layout="wide"
)


# ==================================
# PROJECT PATHS
# ==================================

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "database" / "bridge.db"


# ==================================
# BLACK AND WHITE DESIGN
# ==================================

st.markdown("""
<style>

.stApp {
    background-color: #ffffff;
    color: #000000;
}

[data-testid="stSidebar"] {
    background-color: #f2f2f2;
}

h1, h2, h3, p, label {
    color: #000000;
}

[data-testid="stMetric"] {
    background-color: #f2f2f2;
    border: 1px solid #000000;
    padding: 18px;
    border-radius: 8px;
}

[data-testid="stMetricValue"] {
    color: #000000;
}

[data-testid="stMetricLabel"] {
    color: #444444;
}

.stButton button {
    background-color: #000000;
    color: #ffffff;
    border-radius: 5px;
    border: none;
}

.stButton button:hover {
    background-color: #333333;
    color: #ffffff;
}

</style>
""", unsafe_allow_html=True)


# ==================================
# LOAD DATABASE
# ==================================

@st.cache_data
def load_data():

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        data = pd.read_sql_query(
            "SELECT * FROM integrated_sales",
            connection
        )

        data["sale_date"] = pd.to_datetime(
            data["sale_date"],
            errors="coerce"
        )

        return data

    finally:
        connection.close()


# ==================================
# CHECK DATABASE
# ==================================

st.title("BRIDGE")
st.caption("BUSINESS DATA INTEGRATION AND REPORTING SYSTEM")

st.divider()

if not DATABASE_PATH.exists():
    st.error("Database not found. Please run main.py first.")
    st.stop()

try:
    data = load_data()

except Exception as error:
    st.error(f"Unable to load database: {error}")
    st.stop()

if data.empty:
    st.warning("No sales records available.")
    st.stop()


# ==================================
# SIDEBAR FILTERS
# ==================================

st.sidebar.title("BRIDGE")
st.sidebar.caption("DASHBOARD CONTROLS")

st.sidebar.divider()

st.sidebar.subheader("Filter Sales")

# Date filter
minimum_date = data["sale_date"].min().date()
maximum_date = data["sale_date"].max().date()

selected_dates = st.sidebar.date_input(
    "Select date range",
    value=(minimum_date, maximum_date),
    min_value=minimum_date,
    max_value=maximum_date
)

# Product filter
products = sorted(data["product_name"].dropna().unique())

selected_products = st.sidebar.multiselect(
    "Select products",
    options=products,
    default=products
)

# Category filter
categories = sorted(data["category"].dropna().unique())

selected_categories = st.sidebar.multiselect(
    "Select categories",
    options=categories,
    default=categories
)

st.sidebar.divider()

if st.sidebar.button("Reset Filters"):
    st.rerun()


# ==================================
# APPLY FILTERS
# ==================================

filtered_data = data.copy()

if len(selected_dates) == 2:

    start_date, end_date = selected_dates

    filtered_data = filtered_data[
        (filtered_data["sale_date"].dt.date >= start_date) &
        (filtered_data["sale_date"].dt.date <= end_date)
    ]

filtered_data = filtered_data[
    filtered_data["product_name"].isin(selected_products)
]

filtered_data = filtered_data[
    filtered_data["category"].isin(selected_categories)
]


# ==================================
# BUSINESS OVERVIEW
# ==================================

st.subheader("Business Overview")

if filtered_data.empty:

    st.warning("No records match the selected filters.")

else:

    total_revenue = filtered_data["revenue"].sum()
    total_sales = len(filtered_data)
    total_customers = filtered_data["customer_id"].nunique()
    total_products = filtered_data["product_id"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Revenue",
        f"R{total_revenue:,.2f}"
    )

    col2.metric(
        "Total Sales",
        total_sales
    )

    col3.metric(
        "Customers",
        total_customers
    )

    col4.metric(
        "Products",
        total_products
    )

    st.divider()


    # ==================================
    # REVENUE ANALYSIS
    # ==================================

    st.subheader("Revenue Analysis")

    daily_revenue = (
        filtered_data.groupby("sale_date")["revenue"]
        .sum()
        .sort_index()
    )

    st.line_chart(
        daily_revenue,
        x_label="Sale Date",
        y_label="Revenue (R)"
    )


    # ==================================
    # PRODUCT PERFORMANCE
    # ==================================

    st.divider()

    st.subheader("Product Performance")

    col1, col2 = st.columns(2)

    product_revenue = (
        filtered_data.groupby("product_name")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    with col1:

        st.write("Revenue by Product")
        st.bar_chart(product_revenue)

    with col2:

        st.write("Product Sales Details")

        product_table = (
            filtered_data.groupby("product_name")
            .agg(
                units_sold=("quantity", "sum"),
                total_revenue=("revenue", "sum")
            )
            .reset_index()
            .sort_values(
                "total_revenue",
                ascending=False
            )
        )

        st.dataframe(
            product_table,
            use_container_width=True,
            hide_index=True
        )


    # ==================================
    # CUSTOMER PERFORMANCE
    # ==================================

    st.divider()

    st.subheader("Customer Spending")

    customer_spending = (
        filtered_data.groupby("customer_name")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(customer_spending)


    # ==================================
    # CATEGORY PERFORMANCE
    # ==================================

    st.divider()

    st.subheader("Category Performance")

    col1, col2 = st.columns(2)

    category_revenue = (
        filtered_data.groupby("category")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    with col1:

        st.write("Revenue by Category")
        st.bar_chart(category_revenue)

    with col2:

        st.write("Category Revenue Details")

        st.dataframe(
            category_revenue.reset_index(),
            use_container_width=True,
            hide_index=True
        )


    # ==================================
    # SALES RECORDS
    # ==================================

    st.divider()

    st.subheader("Integrated Sales Records")

    st.dataframe(
        filtered_data,
        use_container_width=True,
        hide_index=True
    )


# ==================================
# FOOTER
# ==================================

st.divider()

st.caption(
    "BRIDGE | Business Intelligence Dashboard | Python • SQL • Streamlit"
)
