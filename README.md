# Bridge Retail – Business Analytics System

## Project Overview

Bridge Retail is a retail business analytics system built with Python, SQL and Power BI.

The project processes retail data from customers, products and sales records. It cleans, validates and integrates the data before storing it in an SQLite database for analysis.

The system generates business insights through SQL queries, data visualisations and interactive dashboards.

## Key Features

- **Data Import:** Imports customer, product and sales data from CSV files.
- **Data Validation:** Checks data quality and identifies invalid records.
- **Data Cleaning:** Prepares datasets for accurate analysis.
- **Data Integration:** Combines multiple datasets into one integrated sales dataset.
- **Database Management:** Stores processed data in SQLite.
- **SQL Analysis:** Analyses sales performance, customer spending and product revenue.
- **Data Visualisation:** Generates charts using Matplotlib.
- **Streamlit Dashboard:** Presents business insights through an interactive dashboard.
- **Power BI Dashboard:** Provides visual analysis of retail performance.
- **Data Export:** Exports integrated sales data for further analysis.

## Technologies Used

- Python
- Pandas
- SQLite
- SQL
- Matplotlib
- Streamlit
- Power BI
- CSV

## Project Structure

```text
Bridge/
│
├── data/
│   ├── raw/
│   └── processed/
│       └── integrated_sales.csv
│
├── database/
│   └── database.py
│
├── src/
│   ├── data_import.py
│   ├── data_validation.py
│   ├── data_cleaning.py
│   ├── data_integration.py
│   ├── data_analysis.py
│   ├── data_visualization.py
│   └── data_export.py
│
├── main.py
├── app.py
├── Bridge_Retail_Dashboard.pbix
└── README.md
```

## Business Insights

The project analyses a fictional retail dataset containing:

- 5 customers
- 5 products
- 8 sales transactions
- Total revenue of **R35,710.00**

### Power BI Dashboard

The Power BI dashboard includes:

**KPI Cards**
- Total Customers: 5
- Total Sales Transactions: 8
- Total Products: 5

**Visualisations**
- Revenue by Product
- Revenue by Customer
- Revenue by Category
- Daily Revenue Trend
- Revenue by City

## Running the Project

### 1. Clone the Repository

```bash
git clone https://github.com/Thando-Khoza/Bridge.git
```

### 2. Open the Project Folder

```bash
cd Bridge
```

### 3. Install Dependencies

```bash
pip install pandas matplotlib streamlit
```

### 4. Run the Main Program

```bash
python main.py
```

### 5. Run the Streamlit Dashboard

```bash
python -m streamlit run app.py
```

## Project Purpose

Bridge Retail demonstrates practical skills in data processing, data cleaning, database management, SQL analysis, business intelligence and data visualisation.

It represents an end-to-end approach to transforming raw retail data into meaningful business insights.

## Author

**Thandolethu Jason Khoza**

Aspiring Software Developer | Python | SQL | Data Analytics
