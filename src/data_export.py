
import sqlite3
import pandas as pd
from pathlib import Path


# Locate project folders
BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "database" / "bridge.db"
EXPORT_DIR = BASE_DIR / "data" / "processed"

EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def export_for_power_bi():
    """Export integrated sales data for Power BI."""

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        data = pd.read_sql_query(
            "SELECT * FROM integrated_sales",
            connection
        )

        if data.empty:
            print("No integrated sales data available.")
            return

        export_path = EXPORT_DIR / "integrated_sales.csv"

        data.to_csv(
            export_path,
            index=False
        )

        print("\nPOWER BI DATA EXPORT")
        print("=" * 35)
        print("Export completed successfully.")
        print(f"Records exported: {len(data)}")
        print(f"File location: {export_path}")

    finally:
        connection.close()


if __name__ == "__main__":
    export_for_power_bi()
