import logging
import sys
from pathlib import Path

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col


INPUT_PATH = "data/raw/messy_raw_pos_data.json"
OUTPUT_PATH = "data/clean/transactions"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def create_spark_session() -> SparkSession:
    return (
        SparkSession.builder
        .appName("RetailDataQuality")
        .config("spark.sql.shuffle.partitions", "4")
        .getOrCreate()
    )


def read_raw_data(spark: SparkSession, input_path: str) -> DataFrame:
    logging.info("Reading raw data from %s", input_path)

    if not Path(input_path).exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    return (
        spark.read
        .option("multiline", "true")
        .json(input_path)
    )


def apply_data_quality_rules(df: DataFrame) -> DataFrame:
    logging.info("Applying data quality rules")

    return (
        df
        .filter(col("store_id").isNotNull())
        .filter(col("raw_price") >= 0)
    )


def deduplicate_transactions(df: DataFrame) -> DataFrame:
    logging.info("Deduplicating transactions by transaction_id")

    return df.dropDuplicates(["transaction_id"])


def write_clean_data(df: DataFrame, output_path: str) -> None:
    logging.info("Writing clean data to %s", output_path)

    (
        df.coalesce(1)
        .write
        .mode("overwrite")
        .parquet(output_path)
    )


def run_data_quality_job(
    spark: SparkSession,
    input_path: str,
    output_path: str,
) -> None:
    raw_df = read_raw_data(spark, input_path)
    raw_count = raw_df.count()
    logging.info("Raw record count: %s", raw_count)

    valid_df = apply_data_quality_rules(raw_df)
    valid_count = valid_df.count()
    logging.info("Record count after quality rules: %s", valid_count)

    deduped_df = deduplicate_transactions(valid_df)
    deduped_count = deduped_df.count()
    logging.info("Record count after deduplication: %s", deduped_count)

    write_clean_data(deduped_df, output_path)

    logging.info("Data quality job completed successfully")


def main() -> None:
    spark = None

    try:
        spark = create_spark_session()
        spark.sparkContext.setLogLevel("ERROR")

        run_data_quality_job(
            spark=spark,
            input_path=INPUT_PATH,
            output_path=OUTPUT_PATH,
        )

    except Exception as error:
        logging.exception("Data quality job failed: %s", error)
        sys.exit(1)

    finally:
        if spark:
            spark.stop()
            logging.info("Spark session stopped")


if __name__ == "__main__":
    main()