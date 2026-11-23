
from src.data_import import import_all_datasets
from src.data_validation import validate_all_datasets
from src.data_cleaning import clean_all_datasets
from src.data_integration import integrate_datasets
from src.data_analysis import analyse_business
from src.data_visualization import create_visualizations

from database.database import (
    create_tables,
    store_integrated_data
)


def main():
    print("\n================================")
    print("       BRIDGE DATA SYSTEM")
    print("================================")

    # STEP 1: Import datasets
    print("\nSTEP 1: IMPORTING DATA")
    customers, products, sales = import_all_datasets()

    # STEP 2: Validate datasets
    print("\nSTEP 2: VALIDATING DATA")
    results = validate_all_datasets(
        customers, products, sales
    )

    # STEP 3: Clean datasets
    print("\nSTEP 3: CLEANING DATA")
    cleaned_customers, cleaned_products, cleaned_sales = (
        clean_all_datasets(customers, products, sales)
    )

    # STEP 4: Integrate datasets
    print("\nSTEP 4: INTEGRATING DATA")
    integrated_data = integrate_datasets(
        cleaned_customers,
        cleaned_products,
        cleaned_sales
    )

    print("\nINTEGRATED SALES DATA")
    print(integrated_data.to_string(index=False))

    # STEP 5: Database storage
    print("\nSTEP 5: DATABASE STORAGE")
    create_tables()
    store_integrated_data(integrated_data)

    # STEP 6: SQL business analysis
    print("\nSTEP 6: SQL BUSINESS ANALYSIS")
    analyse_business()

    # STEP 7: Data visualisation
    print("\nSTEP 7: DATA VISUALISATION")
    create_visualizations()

    # Final summary
    print("\n================================")
    print("       BRIDGE PROCESS SUMMARY")
    print("================================")

    print(f"Customers: {len(cleaned_customers)}")
    print(f"Products: {len(cleaned_products)}")
    print(f"Sales: {len(cleaned_sales)}")
    print(f"Integrated records: {len(integrated_data)}")

    print("\nVALIDATION RESULTS")

    for result in results:
        status = "PASSED" if result["passed"] else "FAILED"
        print(f'{result["dataset"]}: {status}')

    print("\nBridge processing completed successfully.")


if __name__ == "__main__":
    main()

