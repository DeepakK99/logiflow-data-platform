from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    TimestampType,
    IntegerType,
    DoubleType,
    DateType,
    BooleanType,
)

CUSTOMERS_SCHEMA = StructType(
    [
        StructField("customer_id", StringType(), False),
        StructField("company_name", StringType(), False),
        StructField("industry", StringType(), False),
        StructField("customer_tier", StringType(), False),
        StructField("billing_country", StringType(), False),
        StructField("contact_email", StringType(), False),
        StructField("account_status", StringType(), False),
        StructField("created_at", TimestampType(), False),
        StructField("updated_at", TimestampType(), False),
    ]
)

CARRIERS_SCHEMA = StructType(
    [
        StructField("carrier_id", StringType(), False),
        StructField("carrier_name", StringType(), False),
        StructField("service_level", StringType(), False),
        StructField("supported_regions", StringType(), False),
        StructField("contract_status", StringType(), False),
    ]
)

HOLIDAYS_SCHEMA = StructType(
    [
        StructField("holiday_id", StringType(), False),
        StructField("country", StringType(), False),
        StructField("holiday_name", StringType(), False),
        StructField("holiday_date", DateType(), False),
    ]
)

INVENTORY_SCHEMA = StructType(
    [
        StructField("inventory_id", StringType(), False),
        StructField("warehouse_id", StringType(), False),
        StructField("product_id", StringType(), False),
        StructField("available_quantity", IntegerType(), False),
        StructField("reserved_quantity", IntegerType(), False),
        StructField("last_updated", TimestampType(), False),
    ]
)

PRODUCTS_SCHEMA = StructType(
    [
        StructField("product_id", StringType(), False),
        StructField("customer_id", StringType(), False),
        StructField("sku", StringType(), False),
        StructField("product_name", StringType(), False),
        StructField("category", StringType(), False),
        StructField("weight_kg", DoubleType(), False),
        StructField("length_cm", DoubleType(), False),
        StructField("width_cm", DoubleType(), False),
        StructField("height_cm", DoubleType(), False),
        StructField("storage_type", StringType(), False),
        StructField("hazardous_flag", BooleanType(), False),
        StructField("created_at", TimestampType(), False),
        StructField("updated_at", TimestampType(), False),
    ]
)


WAREHOUSES_SCHEMA = StructType(
    [
        StructField("warehouse_id", StringType(), False),
        StructField("warehouse_name", StringType(), False),
        StructField("city", StringType(), False),
        StructField("country", StringType(), False),
        StructField("warehouse_type", StringType(), False),
        StructField("storage_capacity", IntegerType(), False),
        StructField("operational_status", StringType(), False),
        StructField("created_at", TimestampType(), False),
    ]
)

INVENTORY_MOVEMENTS_SCHEMA = StructType(
    [
        StructField("movement_id", StringType(), False),
        StructField("warehouse_id", StringType(), False),
        StructField("product_id", StringType(), False),
        StructField("movement_type", StringType(), False),
        StructField("quantity", IntegerType(), False),
        StructField("movement_timestamp", TimestampType(), False),
    ]
)

SHIPMENT_ITEMS_SCHEMA = StructType(
    [
        StructField("shipment_item_id", StringType(), False),
        StructField("shipment_id", StringType(), False),
        StructField("product_id", StringType(), False),
        StructField("quantity", IntegerType(), False),
        StructField("unit_weight", DoubleType(), False),
    ]
)

SHIPMENTS_SCHEMA = StructType(
    [
        StructField("shipment_id", StringType(), False),
        StructField("customer_id", StringType(), False),
        StructField("origin_warehouse_id", StringType(), False),
        StructField("destination_country", StringType(), False),
        StructField("destination_city", StringType(), False),
        StructField("priority", StringType(), False),
        StructField("shipment_status", StringType(), False),
        StructField("requested_delivery_date", DateType(), False),
        StructField("approved_at", TimestampType(), True),
        StructField("delivered_at", TimestampType(), True),
        StructField("rejection_reason", StringType(), True),
        StructField("created_at", TimestampType(), False),
    ]
)

TRACKING_EVENTS_SCHEMA = StructType(
    [
        StructField("event_id", StringType(), False),
        StructField("shipment_id", StringType(), False),
        StructField("carrier_id", StringType(), False),
        StructField("event_type", StringType(), False),
        StructField("warehouse_id", StringType(), False),
        StructField("event_city", StringType(), False),
        StructField("event_country", StringType(), False),
        StructField("event_timestamp", TimestampType(), False),
    ]
)

WEATHER_SCHEMA = StructType(
    [
        StructField("weather_id", StringType(), False),
        StructField("observation_date", DateType(), False),
        StructField("city", StringType(), False),
        StructField("country", StringType(), False),
        StructField("temperature_c", DoubleType(), False),
        StructField("precipitation_mm", DoubleType(), False),
        StructField("weather_condition", StringType(), False),
    ]
)
