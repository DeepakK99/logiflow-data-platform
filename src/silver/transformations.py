from pyspark.sql.functions import upper, initcap, trim, col


def remove_duplicates(df, primary_keys):

    return df.dropDuplicates(primary_keys)


def standardize_strings(df, config):

    for c in config["uppercase_columns"]:

        df = df.withColumn(
            c,
            upper(trim(col(c)))
        )

    for c in config["titlecase_columns"]:

        df = df.withColumn(
            c,
            initcap(trim(col(c)))
        )

    return df


def validate_required(df, required_columns):

    condition = None

    for c in required_columns:

        expr = col(c).isNotNull()

        if condition is None:

            condition = expr

        else:

            condition &= expr

    valid = df.filter(condition)

    invalid = df.filter(~condition)

    return valid, invalid