# Retail Data Quality & Cost-Optimized BigQuery Modeling

## Project Overview

This project demonstrates a retail data pipeline for cleaning messy POS transaction data and preparing it for analytical use in BigQuery.

The solution covers:

- PySpark data quality processing
- Duplicate removal
- Parquet output for cloud storage
- BigQuery SCD Type 2 product price tracking
- GCP architecture and cost optimization strategy

---

## Task 1: Data Quality Transformation

The PySpark script reads raw JSON POS data from:

```text
data/raw/messy_raw_pos_data.json