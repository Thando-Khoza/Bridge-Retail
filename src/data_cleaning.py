
import pandas as pd


def clean_dataset(data, dataset_name):
    """Clean a copy of an imported dataset."""

    if data is None:
        print(f"Cannot clean {dataset_name}: no data available.")
        return None

    # Preserve the original dataset
    cleaned_data = data.copy()

    original_count = len(cleaned_data)

    print(f"\nCLEANING {dataset_name.upper()}")
    print("=" * 35)

    # Standardise text columns
    text_columns = cleaned_data.select_dtypes(
        include=["object"]
    ).columns

    for column in text_columns:
        cleaned_data[column] = (
            cleaned_data[column]
            .astype("string")
            .str.strip()
        )

        cleaned_data[column] = (
            cleaned_data[column].replace("", pd.NA)
        )

    # Remove duplicate records
    cleaned_data = cleaned_data.drop_duplicates()

    # Remove records with missing required values
    required_columns = {
        "customers": ["customer_id", "customer_name"],
        "products": ["product_id", "product_name", "price"],
        "sales": [
            "sale_id",
            "customer_id",
            "product_id",
            "quantity",
            "sale_date"
        ]
    }

    cleaned_data = cleaned_data.dropna(
        subset=required_columns[dataset_name]
    )

    # Clean product prices
    if dataset_name == "products":
        cleaned_data["price"] = pd.to_numeric(
            cleaned_data["price"],
            errors="coerce"
        )

        cleaned_data = cleaned_data[
            cleaned_data["price"] >= 0
        ]

    # Clean sales quantities and dates
    if dataset_name == "sales":
        cleaned_data["quantity"] = pd.to_numeric(
            cleaned_data["quantity"],
            errors="coerce"
        )

        cleaned_data["sale_date"] = pd.to_datetime(
            cleaned_data["sale_date"],
            errors="coerce"
        )

        cleaned_data = cleaned_data.dropna(
            subset=["quantity", "sale_date"]
        )

        cleaned_data = cleaned_data[
            cleaned_data["quantity"] > 0
        ]

        cleaned_data["quantity"] = (
            cleaned_data["quantity"].astype(int)
        )

        cleaned_data["sale_date"] = (
            cleaned_data["sale_date"].dt.strftime("%Y-%m-%d")
        )

    # Reset row numbering
    cleaned_data = cleaned_data.reset_index(drop=True)

    removed_count = original_count - len(cleaned_data)

    print(f"Original records: {original_count}")
    print(f"Cleaned records: {len(cleaned_data)}")
    print(f"Records removed: {removed_count}")

    return cleaned_data


def clean_all_datasets(customers, products, sales):
    """Clean all three datasets."""

    cleaned_customers = clean_dataset(
        customers, "customers"
    )

    cleaned_products = clean_dataset(
        products, "products"
    )

    cleaned_sales = clean_dataset(
        sales, "sales"
    )

    return (
        cleaned_customers,
        cleaned_products,
        cleaned_sales
    )
