import argparse
import logging
import sys

import psycopg2

from pyspark.sql.functions import col

from src.common.spark import get_spark
from src.common.postgres import get_connection
from src.common.table_config import TABLES
from src.common.config import POSTGRES_CONFIG



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

def truncate_table(table_name: str):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(f"TRUNCATE TABLE staging.{table_name}")
        conn.commit()

    except psycopg2.errors.UndefinedTable:
        conn.rollback()
        print(f"Table staging.{table_name} does not exist yet. Skipping truncation.")

    finally:
        conn.close()

def load_dataset(
    spark,
    dataset_name: str,
    process_date: str | None,
):
    config = TABLES[dataset_name]
    logger.info("Loading %s", dataset_name)

    df = (
        spark.read
        .format("delta")
        .load(config["paths"]["silver"])
    )

    if config["layer"] == "daily":

        if process_date is None:
            raise ValueError(
                f"{dataset_name} requires --process-date"
            )

        df = df.filter(
            col("ingestion_date") == process_date
        )

    technical_columns = [
        "_ingestion_timestamp",
        "_source_file",
    ]

    df = df.drop(*technical_columns)

    row_count = df.count()

    logger.info("Rows : %s", row_count)

    truncate_table(dataset_name)

    (
        df.write
        .format("jdbc")
        .mode("append")
        .option("url", POSTGRES_CONFIG.url)
        .option("driver", "org.postgresql.Driver")
        .option("dbtable", f"staging.{dataset_name}")
        .option("user", POSTGRES_CONFIG.username)
        .option("password", POSTGRES_CONFIG.password)
        .save()
    )

    logger.info("Loaded %s successfully", dataset_name)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--dataset",
        required=True,
        help="Dataset name or all"
    )

    parser.add_argument(
        "--process-date",
        required=False,
    )

    args = parser.parse_args()

    spark = get_spark()

    datasets = (
        TABLES.keys()
        if args.dataset == "all"
        else [args.dataset]
    )

    failed = []

    for dataset in datasets:

        try:

            load_dataset(
                spark=spark,
                dataset_name=dataset,
                process_date=args.process_date,
            )

        except Exception:

            logger.exception(
                "Failed loading %s",
                dataset,
            )

            failed.append(dataset)

    spark.stop()

    if failed:

        logger.error("Failed datasets : %s", failed)
        sys.exit(1)

    logger.info("All datasets loaded successfully")


if __name__ == "__main__":
    main()