import sys
import time

from src.common.table_config import TABLES, file_format
from src.common.spark import get_spark
from src.silver.transformations import (
    remove_duplicates,
    validate_required,
    standardize_strings,
)

from src.common.utils import read_data, write_data

master_deps = {}


def process_table(table_name, process_date):

    config = TABLES[table_name]
    table_type = config["layer"]
    spark = get_spark()

    if table_type == "daily":
        validation_deps = config["deps"]
        for _dep in validation_deps:
            if _dep not in master_deps.keys():
                master_deps[_dep] = read_data(
                    spark, TABLES[_dep]["paths"]["silver"], file_format
                )

    read_params = {
        "spark": spark,
        "path": config["paths"]["bronze"],
        "file_format": file_format,
    }
    if table_type == "daily":
        read_params["filter_column"] = config["partition_coloumn"]
        read_params["filter_value"] = process_date
    df = read_data(**read_params)

    df = remove_duplicates(df, config["primary_key"])

    df, invalid_required = validate_required(df, config["required_columns"])

    df = standardize_strings(df, config)

    validtor_params = {"df": df}

    if table_type == "daily":
        validtor_params |= master_deps
    valid, invalid_business = config["validator"](**validtor_params)

    invalid = invalid_required.unionByName(invalid_business)

    write_params = {
        "df": None,
        "path": config["paths"]["silver"],
        "file_format": file_format,
        "mode": "overwrite",
    }

    if table_type == "daily":
        write_params["partition_column"] = config["partition_coloumn"]

    write_params["df"] = valid
    write_data(**write_params)

    write_params["path"] = config["paths"]["quarentine"]
    write_params["df"] = invalid
    write_data(**write_params)


if __name__ == "__main__":
    process_date = (
        "2026-08-01"  # later use current date(this is just for the data seed)
    )
    print("Starting silver transformation..")
    if len(sys.argv) != 2:
        raise Exception("Usage: python bronze_ingestion.py <table>")

    table = sys.argv[1]

    if table in ["all", "master", "daily"]:
        for table_name in TABLES:
            if table == "all" or TABLES[table_name]["layer"] == table:
                print(f"Ingesting {table_name}...")
                start_time = time.time()
                process_table(table_name, process_date)
                print(
                    f"{table_name} ingested to silver in {round(time.time() - start_time, 2)}s"
                )
    else:
        process_table(table, process_date)
