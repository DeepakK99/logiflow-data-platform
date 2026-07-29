from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

def get_spark():
    builder = (
        SparkSession.builder
        .appName("logiflow")
        .config(
            "spark.sql.extensions",
            "io.delta.sql.DeltaSparkSessionExtension"
        )
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog"
        )
    )

    builder = configure_spark_with_delta_pip(builder)

    packages = builder._options.get("spark.jars.packages", "")
    packages = f"{packages},org.postgresql:postgresql:42.7.4"

    builder = builder.config("spark.jars.packages", packages)

    return builder.getOrCreate()