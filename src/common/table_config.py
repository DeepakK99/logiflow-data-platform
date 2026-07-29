from src.common.schemas import *
from src.common.config import LANDING_DIR, BRONZE_DIR, SILVER_DIR, QUARENTINE_DIR
from src.silver.validators import *

file_format = "delta"

TABLES = {
    "customers": {
        "layer": "master",
        "schema": CUSTOMERS_SCHEMA,
        "primary_key": ["customer_id"],
        "required_columns": [
            "customer_id",
            "company_name",
            "industry",
            "customer_tier",
            "billing_country",
            "contact_email",
            "account_status",
        ],
        "uppercase_columns": ["account_status"],
        "titlecase_columns": ["customer_tier", "billing_country", "industry"],
        "validator": validate_customer,
        "paths": {
            "landing": str(LANDING_DIR / "master" / "customers.csv"),
            "bronze": str(BRONZE_DIR / "master" / "customers"),
            "silver": str(SILVER_DIR / "master" / "customers"),
            "quarentine": str(QUARENTINE_DIR / "master" / "customers"),
        },
    },
    "carriers": {
        "layer": "master",
        "schema": CARRIERS_SCHEMA,
        "primary_key": ["carrier_id"],
        "required_columns": [
            "carrier_id",
            "carrier_name",
            "service_level",
            "supported_regions",
            "contract_status",
        ],
        "uppercase_columns": ["service_level", "contract_status"],
        "titlecase_columns": ["carrier_name"],
        "validator": validate_carriers,
        "paths": {
            "landing": str(LANDING_DIR / "master" / "carriers.csv"),
            "bronze": str(BRONZE_DIR / "master" / "carriers"),
            "silver": str(SILVER_DIR / "master" / "carriers"),
            "quarentine": str(QUARENTINE_DIR / "master" / "carriers"),
        },
    },
    "holidays": {
        "layer": "master",
        "schema": HOLIDAYS_SCHEMA,
        "primary_key": ["holiday_id"],
        "required_columns": ["holiday_id", "country", "holiday_name", "holiday_date"],
        "uppercase_columns": [],
        "titlecase_columns": ["country", "holiday_name"],
        "validator": validate_holidays,
        "paths": {
            "landing": str(LANDING_DIR / "master" / "holidays.csv"),
            "bronze": str(BRONZE_DIR / "master" / "holidays"),
            "silver": str(SILVER_DIR / "master" / "holidays"),
            "quarentine": str(QUARENTINE_DIR / "master" / "holidays"),
        },
    },
    "products": {
        "layer": "master",
        "schema": PRODUCTS_SCHEMA,
        "primary_key": ["product_id"],
        "required_columns": [
            "product_id",
            "customer_id",
            "sku",
            "product_name",
            "category",
            "weight_kg",
            "length_cm",
            "width_cm",
            "height_cm",
            "storage_type",
            "hazardous_flag",
            "created_at",
            "updated_at",
        ],
        "uppercase_columns": ["storage_type"],
        "titlecase_columns": ["category"],
        "validator": validate_product,
        "paths": {
            "landing": str(LANDING_DIR / "master" / "products.csv"),
            "bronze": str(BRONZE_DIR / "master" / "products"),
            "silver": str(SILVER_DIR / "master" / "products"),
            "quarentine": str(QUARENTINE_DIR / "master" / "products"),
        },
    },
    "warehouses": {
        "layer": "master",
        "schema": WAREHOUSES_SCHEMA,
        "primary_key": ["warehouse_id"],
        "required_columns": [
            "warehouse_id",
            "warehouse_name",
            "city",
            "country",
            "warehouse_type",
            "storage_capacity",
            "operational_status",
            "created_at",
        ],
        "uppercase_columns": ["warehouse_type", "operational_status"],
        "titlecase_columns": ["warehouse_name", "city", "country"],
        "validator": validate_warehouse,
        "paths": {
            "landing": str(LANDING_DIR / "master" / "warehouses.csv"),
            "bronze": str(BRONZE_DIR / "master" / "warehouses"),
            "silver": str(SILVER_DIR / "master" / "warehouses"),
            "quarentine": str(QUARENTINE_DIR / "master" / "warehouses"),
        },
    },
    "inventory": {
        "layer": "daily",
        "schema": INVENTORY_SCHEMA,
        "primary_key": ["inventory_id"],
        "required_columns": [
            "inventory_id",
            "warehouse_id",
            "product_id",
            "available_quantity",
            "reserved_quantity",
            "last_updated",
        ],
        "uppercase_columns": [],
        "titlecase_columns": [],
        "validator": validate_inventory,
        "paths": {
            "landing": str(
                            LANDING_DIR
                            / "daily"
                            / "ingestion_date={ingestion_date}"
                            / "inventory.csv"
                        ),
            "bronze": str(BRONZE_DIR / "daily" / "inventory"),
            "silver": str(SILVER_DIR / "daily" / "inventory"),
            "quarentine": str(QUARENTINE_DIR / "daily" / "inventory"),
        },
        "deps": ["warehouses", "products"],
        "partition_coloumn": "ingestion_date",
    },
    "inventory_movements": {
        "layer": "daily",
        "schema": INVENTORY_MOVEMENTS_SCHEMA,
        "primary_key": ["movement_id"],
        "required_columns": [
            "movement_id",
            "warehouse_id",
            "product_id",
            "movement_type",
            "quantity",
            "movement_timestamp",
        ],
        "uppercase_columns": ["movement_type"],
        "titlecase_columns": [],
        "validator": validate_inventory_movement,
        "paths": {
            "landing": str(
                LANDING_DIR
                / "daily"
                / "ingestion_date={ingestion_date}"
                / "inventory_movements.csv"
            ),
            "bronze": str(BRONZE_DIR / "daily" / "inventory_movements"),
            "silver": str(SILVER_DIR / "daily" / "inventory_movements"),
            "quarentine": str(QUARENTINE_DIR / "daily" / "inventory_movements"),
        },
        "deps": ["warehouses", "products"],
        "partition_coloumn": "ingestion_date",
    },
    "shipments": {
        "layer": "daily",
        "schema": SHIPMENTS_SCHEMA,
        "primary_key": ["shipment_id"],
        "required_columns": [
            "shipment_id",
            "customer_id",
            "origin_warehouse_id",
            "destination_country",
            "destination_city",
            "priority",
            "shipment_status",
            "requested_delivery_date",
            "created_at",
        ],
        "uppercase_columns": ["priority", "shipment_status"],
        "titlecase_columns": ["destination_country", "destination_city"],
        "validator": validate_shipment,
        "paths": {
            "landing": str(
                LANDING_DIR
                / "daily"
                / "ingestion_date={ingestion_date}"
                / "shipments.csv"
            ),
            "bronze": str(BRONZE_DIR / "daily" / "shipments"),
            "silver": str(SILVER_DIR / "daily" / "shipments"),
            "quarentine": str(QUARENTINE_DIR / "daily" / "shipments"),
        },
        "deps": ["customers", "warehouses"],
        "partition_coloumn": "ingestion_date",
    },
    "shipment_items": {
        "layer": "daily",
        "schema": SHIPMENT_ITEMS_SCHEMA,
        "primary_key": ["shipment_item_id"],
        "required_columns": [
            "shipment_item_id",
            "shipment_id",
            "product_id",
            "quantity",
            "unit_weight",
        ],
        "uppercase_columns": [],
        "titlecase_columns": [],
        "validator": validate_shipment_item,
        "paths": {
            "landing": str(
                LANDING_DIR
                / "daily"
                / "ingestion_date={ingestion_date}"
                / "shipment_items.csv"
            ),
            "bronze": str(BRONZE_DIR / "daily" / "shipment_items"),
            "silver": str(SILVER_DIR / "daily" / "shipment_items"),
            "quarentine": str(QUARENTINE_DIR / "daily" / "shipment_items"),
        },
        "deps": ["shipments", "products"],
        "partition_coloumn": "ingestion_date",
    },
    "tracking_events": {
        "layer": "daily",
        "schema": TRACKING_EVENTS_SCHEMA,
        "primary_key": ["event_id"],
        "required_columns": [
            "event_id",
            "shipment_id",
            "carrier_id",
            "event_type",
            "warehouse_id",
            "event_city",
            "event_country",
            "event_timestamp",
        ],
        "uppercase_columns": ["event_type"],
        "titlecase_columns": ["event_city", "event_country"],
        "validator": validate_tracking_event,
        "paths": {
            "landing": str(
                LANDING_DIR
                / "daily"
                / "ingestion_date={ingestion_date}"
                / "tracking_events.csv"
            ),
            "bronze": str(BRONZE_DIR / "daily" / "tracking_events"),
            "silver": str(SILVER_DIR / "daily" / "tracking_events"),
            "quarentine": str(QUARENTINE_DIR / "daily" / "tracking_events"),
        },
        "deps": ["shipments", "carriers", "warehouses"],
        "partition_coloumn": "ingestion_date",
    },
    "weather": {
        "layer": "daily",
        "schema": WEATHER_SCHEMA,
        "primary_key": ["weather_id"],
        "required_columns": [
            "weather_id",
            "observation_date",
            "city",
            "country",
            "temperature_c",
            "precipitation_mm",
            "weather_condition",
        ],
        "uppercase_columns": ["weather_condition"],
        "titlecase_columns": ["city", "country"],
        "validator": validate_weather,
        "paths": {
            "landing": str(
                LANDING_DIR
                / "daily"
                / "ingestion_date={ingestion_date}"
                / "weather.csv"
            ),
            "bronze": str(BRONZE_DIR / "daily" / "weather"),
            "silver": str(SILVER_DIR / "daily" / "weather"),
            "quarentine": str(QUARENTINE_DIR / "daily" / "weather"),
        },
        "deps": [],
        "partition_coloumn": "ingestion_date",
    },
}
