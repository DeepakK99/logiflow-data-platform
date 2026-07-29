from pyspark.sql import functions as F

def read_data(spark, path, file_format: str, filter_column: str = None, filter_value=None):
    reader = spark.read.format(file_format)
    
    if file_format.lower() == "csv":
        reader = reader.option("header", "true").option("inferSchema", "true")
        
    df = reader.load(path)

    if filter_column is not None and filter_value is not None:
        df = df.filter(F.col(filter_column) == filter_value)

    return df




def write_data(df, path, file_format: str, mode, partition_column: str = None):
    writer = df.write.mode(mode).format(file_format)

    if partition_column is not None:
        writer = writer.partitionBy(partition_column)

    writer.save(path)

