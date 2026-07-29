import sys
import time

from pyspark.sql.functions import (
    current_timestamp,
    input_file_name,
)

from src.common.spark import get_spark
from src.common.table_config import TABLES, file_format

from src.common.utils import read_data, write_data

def ingest(table_name, process_date):

    if table_name not in TABLES:
        raise ValueError(f"Unknown table: {table_name}")

    config = TABLES[table_name]

    spark = get_spark()

    # df = (
    #     spark.read.option("header", True)
    #     .schema(config["schema"])
    #     .csv(
    #         config["paths"]["landing"].format(ingestion_date=ingestion_date)
    #         if config["layer"] == "daily"
    #         else config["paths"]["landing"]
    #     )
    # )
    df = read_data(spark, config["paths"]["landing"].format(ingestion_date=process_date)
                if config["layer"] == "daily"
                else config["paths"]["landing"], "csv")

    df = df.withColumn("_ingestion_timestamp", current_timestamp()).withColumn(
        "_source_file", input_file_name()
    )

    if config["layer"] == "master":
        # (df.write.mode("overwrite").format(file_format).save(config["paths"]["bronze"]))
        write_data(df, config["paths"]["bronze"], file_format, "overwrite")
    elif config["layer"] == "daily":
        from pyspark.sql.functions import lit

        df = df.withColumn("ingestion_date", lit(process_date))

        # (
        #     df.write.mode("append")
        #     .format(file_format)
        #     .partitionBy("ingestion_date")
        #     .save(config["paths"]["bronze"])
        # )
        write_data(df, config["paths"]["bronze"], file_format, "overwrite", "ingestion_date")


if __name__ == "__main__":
    process_date = (
        "2026-08-01"  # later use current date(this is just for the data seed)
    )
    print("Starting bronze transformation..")
    if len(sys.argv) != 2:
        raise Exception("Usage: python bronze_ingestion.py <table>")

    table = sys.argv[1]

    if table in ["all", "master", "daily"]:
        for table_name in TABLES:
            if table == "all" or TABLES[table_name]["layer"] == table:
                print(f"Ingesting {table_name}...")
                start_time = time.time()
                ingest(table_name, process_date)
                print(
                    f"{table_name} ingested to bronze in {round(time.time() - start_time, 2)}s"
                )
    else:
        ingest(table, process_date)
