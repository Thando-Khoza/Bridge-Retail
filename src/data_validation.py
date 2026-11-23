
import pandas as pd


REQUIRED_COLUMNS = {
    "customers": [
        "customer_id",
        "customer_name",
        "city"
    ],
    "products": [
        "product_id",
        "product_name",
        "category",
        "price"
    ],
    "sales": [
        "sale_id",
        "customer_id",
        "product_id",
        "quantity",
        "sale_date"
    ]
}


def validate_columns(data, dataset_name):
    """Check whether all required columns exist."""

    required = REQUIRED_COLUMNS[dataset_name]
    missing_columns = [
        column for column in required
        if column not in data.columns
    ]

    if missing_columns:
        return False, missing_columns

    return True, []


def validate_dataset(data, dataset_name):
    """Check a dataset for common data-quality problems."""

    print(f"\nVALIDATING {dataset_name.upper()}")
    print("=" * 35)

    if data is None:
        print("Dataset could not be loaded.")
        return None

    valid_columns, missing_columns = validate_columns(
        data, dataset_name
    )

    if not valid_columns:
        print(f"Missing columns: {missing_columns}")
        return None

    errors = []

    # Check missing values
    missing_values = int(data.isnull().sum().sum())

    if missing_values:
        errors.append(f"Missing values: {missing_values}")

    # Check duplicate rows
    duplicates = int(data.duplicated().sum())

    if duplicates:
        errors.append(f"Duplicate rows: {duplicates}")

    # Check duplicate IDs
    id_column = {
        "customers": "customer_id",
        "products": "product_id",
        "sales": "sale_id"
    }[dataset_name]

    duplicate_ids = int(data[id_column].duplicated().sum())

    if duplicate_ids:
        errors.append(f"Duplicate IDs: {duplicate_ids}")

    # Check product prices
    if dataset_name == "products":
        prices = pd.to_numeric(
            data["price"], errors="coerce"
        )

        invalid_prices = int(
            (prices.isna() | (prices < 0)).sum()
        )

        if invalid_prices:
            errors.append(f"Invalid prices: {invalid_prices}")

    # Check sales quantities
    if dataset_name == "sales":
        quantities = pd.to_numeric(
            data["quantity"], errors="coerce"
        )

        invalid_quantities = int(
            (quantities.isna() | (quantities <= 0)).sum()
        )

        if invalid_quantities:
            errors.append(
                f"Invalid quantities: {invalid_quantities}"
            )

        # Validate sale dates
        dates = pd.to_datetime(
            data["sale_date"], errors="coerce"
        )

        invalid_dates = int(dates.isna().sum())

        if invalid_dates:
            errors.append(f"Invalid dates: {invalid_dates}")

    # Display results
    if errors:
        print("Validation completed with issues:")

        for error in errors:
            print(f"- {error}")
    else:
        print("All validation checks passed.")

    print(f"Total records: {len(data)}")
    print(f"Missing values: {missing_values}")
    print(f"Duplicate rows: {duplicates}")

    return {
        "dataset": dataset_name,
        "total_records": len(data),
        "missing_values": missing_values,
        "duplicate_rows": duplicates,
        "issues": errors,
        "passed": len(errors) == 0
    }


def validate_all_datasets(customers, products, sales):
    """Validate all three Bridge datasets."""

    results = []

    datasets = [
        (customers, "customers"),
        (products, "products"),
        (sales, "sales")
    ]

    for data, name in datasets:
        result = validate_dataset(data, name)

        if result is not None:
            results.append(result)

    return results
