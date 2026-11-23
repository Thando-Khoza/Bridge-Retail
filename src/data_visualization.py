
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# Locate project folders
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "database" / "bridge.db"
REPORTS_DIR = BASE_DIR / "reports"

# Create reports folder if it doesn't exist
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def load_integrated_data():
    """Load integrated sales data from SQLite."""

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        data = pd.read_sql_query(
            "SELECT * FROM integrated_sales",
            connection
        )
        return data

    finally:
        connection.close()


def create_visualizations():
    """Generate business charts using Matplotlib."""

    data = load_integrated_data()

    if data.empty:
        print("No integrated sales data available.")
        return

    print("\nDATA VISUALISATION")
    print("=" * 40)

    # 1. Daily revenue trend
    daily_revenue = (
        data.groupby("sale_date")["revenue"]
        .sum()
        .sort_index()
    )

    plt.figure(figsize=(10, 5))
    daily_revenue.plot(kind="line", marker="o")

    plt.title("Daily Revenue Trend")
    plt.xlabel("Sale Date")
    plt.ylabel("Revenue (R)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(REPORTS_DIR / "daily_revenue.png")
    plt.close()

    print("Created: daily_revenue.png")

    # 2. Product performance
    product_revenue = (
        data.groupby("product_name")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(10, 5))
    product_revenue.plot(kind="bar")

    plt.title("Revenue by Product")
    plt.xlabel("Product")
    plt.ylabel("Revenue (R)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(REPORTS_DIR / "product_performance.png")
    plt.close()

    print("Created: product_performance.png")

    # 3. Customer spending
    customer_spending = (
        data.groupby("customer_name")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(10, 5))
    customer_spending.plot(kind="bar")

    plt.title("Customer Spending")
    plt.xlabel("Customer")
    plt.ylabel("Total Spending (R)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(REPORTS_DIR / "customer_spending.png")
    plt.close()

    print("Created: customer_spending.png")

    # 4. Category revenue
    category_revenue = (
        data.groupby("category")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(8, 8))
    category_revenue.plot(
        kind="pie",
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Revenue by Category")
    plt.ylabel("")
    plt.tight_layout()

    plt.savefig(REPORTS_DIR / "category_revenue.png")
    plt.close()

    print("Created: category_revenue.png")

    print("\nAll four visualisations created successfully.")
    print(f"Charts saved in: {REPORTS_DIR}")


if __name__ == "__main__":
    create_visualizations()
