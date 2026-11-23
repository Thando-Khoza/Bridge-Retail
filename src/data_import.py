
import pandas as pd
from pathlib import Path


# Locate the project folders
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"


def import_csv(file_name):
    """
    Import a CSV file from the raw data folder.
    """

    file_path = RAW_DATA_DIR / file_name

    # Check whether the file exists
    if not file_path.exists():
        print(f"Error: {file_name} was not found.")
        return None

    try:
        # Read the CSV file
        data = pd.read_csv(file_path)

        print(f"\nSuccessfully imported: {file_name}")
        print(f"Records found: {len(data)}")

        return data

    except pd.errors.EmptyDataError:
        print(f"Error: {file_name} is empty.")
        return None

    except (pd.errors.ParserError, UnicodeDecodeError) as error:
        print(f"Error reading {file_name}: {error}")
        return None

    except OSError as error:
        print(f"File error: {error}")
        return None


def import_all_datasets():
    """
    Import all three Bridge datasets.
    """

    customers = import_csv("customers.csv")
    products = import_csv("products.csv")
    sales = import_csv("sales.csv")

    return customers, products, sales


if __name__ == "__main__":

    print("BRIDGE CSV IMPORT SYSTEM")
    print("========================")

    customers, products, sales = import_all_datasets()

    print("\nImport process completed.")
