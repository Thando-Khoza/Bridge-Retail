
def integrate_datasets(customers, products, sales):
    """
    Combine customers, products and sales into one dataset.
    """

    print("\nINTEGRATING DATASETS")
    print("=" * 35)

    # Connect sales to customer information
    integrated_data = sales.merge(
        customers,
        on="customer_id",
        how="left"
    )

    # Connect sales to product information
    integrated_data = integrated_data.merge(
        products,
        on="product_id",
        how="left"
    )

    # Calculate total revenue for each sale
    integrated_data["revenue"] = (
        integrated_data["quantity"] *
        integrated_data["price"]
    )

    # Arrange columns in a useful order
    integrated_data = integrated_data[
        [
            "sale_id",
            "sale_date",
            "customer_id",
            "customer_name",
            "city",
            "product_id",
            "product_name",
            "category",
            "quantity",
            "price",
            "revenue"
        ]
    ]

    print("Data integration completed successfully.")
    print(f"Integrated records: {len(integrated_data)}")

    return integrated_data
