import os

from pyspark.sql import SparkSession

from scripts.data_quality import (
    apply_data_quality_rules,
    deduplicate_transactions,
)

PYTHON_PATH = r"C:\Users\pamposwa\AppData\Local\Programs\Python\Python312\python.exe"

os.environ["PYSPARK_PYTHON"] = PYTHON_PATH
os.environ["PYSPARK_DRIVER_PYTHON"] = PYTHON_PATH


def create_test_spark_session():
    return (
        SparkSession.builder
        .master("local[1]")
        .appName("unit-test")
        .getOrCreate()
    )


def test_apply_data_quality_rules():
    spark = create_test_spark_session()

    data = [
        ("tx1", "STORE_001", 100.0),
        ("tx2", None, 50.0),
        ("tx3", "STORE_002", -10.0),
    ]

    columns = [
        "transaction_id",
        "store_id",
        "raw_price",
    ]

    df = spark.createDataFrame(data, columns)

    result_df = apply_data_quality_rules(df)

    assert result_df.count() == 1

    spark.stop()


def test_deduplicate_transactions():
    spark = create_test_spark_session()

    data = [
        ("tx1",),
        ("tx1",),
        ("tx2",),
    ]

    columns = ["transaction_id"]

    df = spark.createDataFrame(data, columns)

    result_df = deduplicate_transactions(df)

    assert result_df.count() == 2

    spark.stop()