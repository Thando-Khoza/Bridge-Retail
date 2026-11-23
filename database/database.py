
import sqlite3
import pandas as pd
from pathlib import Path


# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database location
DATABASE_PATH = BASE_DIR / "database" / "bridge.db"


def create_connection():
    """Create a connection to the Bridge database."""

    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def create_tables():
    """Create all database tables."""

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT PRIMARY KEY,
            customer_name TEXT NOT NULL,
            city TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT,
            price REAL NOT NULL CHECK(price >= 0)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            sale_id TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            product_id TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            sale_date TEXT NOT NULL,

            FOREIGN KEY (customer_id)
                REFERENCES customers(customer_id),

            FOREIGN KEY (product_id)
                REFERENCES products(product_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS import_history (
            import_id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            imported_at TEXT DEFAULT CURRENT_TIMESTAMP,
            records_imported INTEGER DEFAULT 0,
            status TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data_quality_reports (
            report_id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            total_records INTEGER DEFAULT 0,
            valid_records INTEGER DEFAULT 0,
            invalid_records INTEGER DEFAULT 0,
            duplicate_records INTEGER DEFAULT 0,
            checked_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()

    print("Bridge database tables are ready.")


def store_integrated_data(integrated_data):
    """Store integrated sales data in SQLite."""

    connection = create_connection()

    try:
        integrated_data.to_sql(
            "integrated_sales",
            connection,
            if_exists="replace",
            index=False
        )

        print("\nDATABASE STORAGE")
        print("=" * 35)
        print("Integrated data stored successfully.")
        print(f"Records stored: {len(integrated_data)}")

    finally:
        connection.close()


if __name__ == "__main__":
    create_tables()

import sqlite3
import pandas as pd
from pathlib import Path


# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database location
DATABASE_PATH = BASE_DIR / "database" / "bridge.db"


def create_connection():
    """Create a connection to the Bridge database."""

    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def create_tables():
    """Create all database tables."""

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT PRIMARY KEY,
            customer_name TEXT NOT NULL,
            city TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT,
            price REAL NOT NULL CHECK(price >= 0)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            sale_id TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            product_id TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            sale_date TEXT NOT NULL,

            FOREIGN KEY (customer_id)
                REFERENCES customers(customer_id),

            FOREIGN KEY (product_id)
                REFERENCES products(product_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS import_history (
            import_id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            imported_at TEXT DEFAULT CURRENT_TIMESTAMP,
            records_imported INTEGER DEFAULT 0,
            status TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data_quality_reports (
            report_id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            total_records INTEGER DEFAULT 0,
            valid_records INTEGER DEFAULT 0,
            invalid_records INTEGER DEFAULT 0,
            duplicate_records INTEGER DEFAULT 0,
            checked_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()

    print("Bridge database tables are ready.")


def store_integrated_data(integrated_data):
    """Store integrated sales data in SQLite."""

    connection = create_connection()

    try:
        integrated_data.to_sql(
            "integrated_sales",
            connection,
            if_exists="replace",
            index=False
        )

        print("\nDATABASE STORAGE")
        print("=" * 35)
        print("Integrated data stored successfully.")
        print(f"Records stored: {len(integrated_data)}")

    finally:
        connection.close()


if __name__ == "__main__":
    create_tables()

