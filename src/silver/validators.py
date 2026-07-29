from pyspark.sql.functions import col
from src.common.constants import *


def validate_customer(df):

    valid = df.filter(col("customer_tier").isin(VALID_TIERS)).filter(
        col("account_status").isin(VALID_STATUS)
    )

    invalid = df.subtract(valid)

    return valid, invalid


def validate_carriers(df):

    valid = df.filter(col("service_level").isin(VALID_SERVICE_LEVELS)).filter(
        col("contract_status").isin(VALID_CONTRACT_STATUS)
    )

    invalid = df.subtract(valid)

    return valid, invalid


def validate_holidays(df):
    valid = df.filter(
        col("country").isin(VALID_COUNTRIES) & col("holiday_date").isNotNull()
    )

    invalid = df.subtract(valid)

    return valid, invalid

def validate_product(df):

    valid = (
        df.filter(col("weight_kg") > 0)
        .filter(col("length_cm") > 0)
        .filter(col("width_cm") > 0)
        .filter(col("height_cm") > 0)
        .filter(col("storage_type").isin(VALID_STORAGE_TYPES))
    )

    invalid = df.subtract(valid)

    return valid, invalid


def validate_warehouse(df):

    valid = (
        df.filter(col("storage_capacity") > 0)
        .filter(col("warehouse_type").isin(VALID_WAREHOUSE_TYPES))
        .filter(col("operational_status").isin(VALID_OPERATIONAL_STATUS))
    )

    invalid = df.subtract(valid)

    return valid, invalid


def validate_inventory(df, **kwargs):
    warehouse_df = kwargs["warehouses"]
    product_df = kwargs["products"]

    valid = (
        df.filter(col("available_quantity") >= 0)
        .filter(col("reserved_quantity") >= 0)
        .filter(col("reserved_quantity") <= col("available_quantity"))
        .join(warehouse_df.select("warehouse_id"), "warehouse_id", "inner")
        .join(product_df.select("product_id"), "product_id", "inner")
    )

    invalid = df.subtract(valid)

    return valid, invalid

def validate_inventory_movement(df, **kwargs):

    warehouse_df = kwargs["warehouses"]
    product_df = kwargs["products"]

    valid = (
        df.filter(col("quantity") > 0)
        .filter(col("movement_type").isin(VALID_MOVEMENT_TYPES))
        .join(warehouse_df.select("warehouse_id"), "warehouse_id", "inner")
        .join(product_df.select("product_id"), "product_id", "inner")
    )

    invalid = df.subtract(valid)

    return valid, invalid


def validate_shipment_item(df, **kwargs):

    shipments = kwargs["shipments"]
    products = kwargs["products"]

    valid = (
        df.filter(col("quantity") > 0)
        .filter(col("unit_weight") > 0)
        .join(shipments.select("shipment_id"), "shipment_id", "inner")
        .join(products.select("product_id"), "product_id", "inner")
    )

    invalid = df.subtract(valid)

    return valid, invalid


def validate_shipment(df, **kwargs):

    customers = kwargs["customers"]
    warehouses = kwargs["warehouses"]

    valid = (
        df.filter(col("priority").isin(VALID_PRIORITIES))
        .filter(col("shipment_status").isin(VALID_SHIPMENT_STATUS))
        .filter(
            ~(
                (col("shipment_status") == "REJECTED")
                & (col("rejection_reason").isNull())
            )
        )
        .filter(
            ~((col("shipment_status") == "DELIVERED") & (col("delivered_at").isNull()))
        )
        .filter(
            ~(
                (col("approved_at").isNotNull())
                & (col("approved_at") < col("created_at"))
            )
        )
        .join(customers.select("customer_id"), "customer_id", "inner")
        .join(
            warehouses.select("warehouse_id"),
            col("origin_warehouse_id") == warehouses["warehouse_id"],
            "inner",
        )
        .drop(warehouses["warehouse_id"])
    )

    invalid = df.subtract(valid)

    return valid, invalid


def validate_tracking_event(df, **kwargs):

    shipments = kwargs["shipments"]
    carriers = kwargs["carriers"]
    warehouses = kwargs["warehouses"]

    valid = (
        df.filter(col("event_type").isin(VALID_EVENT_TYPES))
        .join(shipments.select("shipment_id"), "shipment_id", "inner")
        .join(carriers.select("carrier_id"), "carrier_id", "inner")
        .join(warehouses.select("warehouse_id"), "warehouse_id", "inner")
    )

    invalid = df.subtract(valid)

    return valid, invalid


def validate_weather(df, **kwargs):

    valid = (
        df.filter(col("temperature_c").between(-50, 60))
        .filter(col("precipitation_mm") >= 0)
        .filter(col("weather_condition").isin(VALID_WEATHER_CONDITIONS))
    )

    invalid = df.subtract(valid)

    return valid, invalid
