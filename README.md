# Retail Data Quality & Cost-Optimized BigQuery Modeling

## Overview

This project demonstrates a retail data pipeline for processing messy point-of-sale (POS) transaction data and preparing it for analytics in Google BigQuery.

The solution addresses:

- Data quality validation using PySpark
- Duplicate removal
- Cloud-optimized storage using Parquet
- Historical product price tracking using Slowly Changing Dimension Type 2 (SCD Type 2)
- Cost optimization strategies for BigQuery

---

# Tech Stack

- Python 3.12
- PySpark 4.1.2
- BigQuery SQL
- Java 17

---

# Project Structure

```text
retail-data-quality-bigquery
│
├── data
│   ├── raw
│   └── clean
│
├── scripts
│   └── data_quality.py
│
├── sql
│   └── scd_type_2.sql
│
├── tests
│   └── test_data_quality.py
│
├── generate_data.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Task 1 – Data Quality Transformation

The PySpark script performs the following validations:

- Removes records with null store_id.
- Removes records with negative raw_price.
- Removes duplicate records using transaction_id.
- Writes clean data in Parquet format.

Input:

```text
data/raw/messy_raw_pos_data.json
```

Output:

```text
data/clean/transactions
```

---

# Task 2 – Slowly Changing Dimension Type 2

The SQL script located in:

```text
sql/scd_type_2.sql
```

tracks historical product price changes.

When a product price changes:

- The existing record is expired.
- The effective_end_date is updated.
- A new current record is inserted.
- Historical prices are preserved.

---

# Task 3 – GCP Architecture

## Proposed Architecture

```text
Raw JSON Files
        |
        v
Cloud Storage (Raw Zone)
        |
        v
Dataproc Serverless / Cloud Run
        |
        v
Cloud Storage (Parquet)
        |
        v
BigQuery Staging Table
        |
        v
SCD Type 2 Merge
        |
        v
Dim_Product
        |
        v
Fact_Daily_Sales
        |
        v
Looker Studio
```

---

# BigQuery Cost Optimization

## Partitioning

Fact tables should be partitioned by:

```sql
transaction_date
```

Example:

```sql
PARTITION BY DATE(transaction_date)
```

This minimizes the amount of data scanned during queries.

---

## Clustering

Tables should be clustered by:

```sql
store_id, product_id
```

This improves query performance for reporting workloads.

---

## Recommended Tables

- stg_clean_transactions
- dim_product
- fact_daily_sales

---

# Running the Project

## Install dependencies

```bash
pip install -r requirements.txt
```

## Generate sample data

```bash
python generate_data.py
```

## Execute the PySpark job

```bash
python scripts\data_quality.py
```

---

# Author

Phindile Mposwa