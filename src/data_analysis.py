
import sqlite3
from pathlib import Path


# Locate the Bridge database
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "database" / "bridge.db"


def run_query(query):
    """Execute an SQL query and return its results."""

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results

    finally:
        connection.close()


def analyse_business():
    """Generate business insights using SQL."""

    print("\nSQL BUSINESS ANALYSIS")
    print("=" * 40)

    # 1. Total revenue
    revenue = run_query("""
        SELECT SUM(revenue)
        FROM integrated_sales
    """)

    print(f"\nTotal Revenue: R{revenue[0][0]:,.2f}")

    # 2. Best-selling products by revenue
    products = run_query("""
        SELECT
            product_name,
            SUM(quantity) AS units_sold,
            SUM(revenue) AS total_revenue
        FROM integrated_sales
        GROUP BY product_name
        ORDER BY total_revenue DESC
    """)

    print("\nPRODUCT PERFORMANCE")
    print("-" * 40)

    for product in products:
        print(
            f"{product[0]} | "
            f"Units: {product[1]} | "
            f"Revenue: R{product[2]:,.2f}"
        )

    # 3. Customer spending
    customers = run_query("""
        SELECT
            customer_name,
            SUM(revenue) AS total_spent
        FROM integrated_sales
        GROUP BY customer_name
        ORDER BY total_spent DESC
    """)

    print("\nCUSTOMER SPENDING")
    print("-" * 40)

    for customer in customers:
        print(
            f"{customer[0]} | "
            f"Spent: R{customer[1]:,.2f}"
        )

    # 4. Revenue by category
    categories = run_query("""
        SELECT
            category,
            SUM(revenue) AS total_revenue
        FROM integrated_sales
        GROUP BY category
        ORDER BY total_revenue DESC
    """)

    print("\nCATEGORY PERFORMANCE")
    print("-" * 40)

    for category in categories:
        print(
            f"{category[0]} | "
            f"Revenue: R{category[1]:,.2f}"
        )

    # 5. Daily revenue
    daily_revenue = run_query("""
        SELECT
            sale_date,
            SUM(revenue) AS total_revenue
        FROM integrated_sales
        GROUP BY sale_date
        ORDER BY sale_date
    """)

    print("\nDAILY REVENUE")
    print("-" * 40)

    for day in daily_revenue:
        print(
            f"{day[0]} | "
            f"Revenue: R{day[1]:,.2f}"
        )


if __name__ == "__main__":
    analyse_business()
