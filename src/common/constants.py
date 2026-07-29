# customers
VALID_TIERS = ["Gold", "Silver", "Bronze"]

VALID_STATUS = ["ACTIVE", "INACTIVE"]

# carriers
VALID_SERVICE_LEVELS = ["STANDARD", "EXPRESS"]

VALID_CONTRACT_STATUS = ["ACTIVE", "INACTIVE"]

# tracking events

VALID_EVENT_TYPES = [
    "REQUESTED",
    "APPROVED",
    "PICKED_UP",
    "IN_TRANSIT",
    "OUT_FOR_DELIVERY",
    "DELIVERED",
    "REJECTED"
]

# holidays
VALID_COUNTRIES = [
    "India",
    "United States",
    "Germany",
    "United Kingdom",
    "Singapore",
    "Australia",
    "Japan",
    "Canada"
]

# products
VALID_STORAGE_TYPES = [
    "AMBIENT",
    "REFRIGERATED",
    "FROZEN"
]

# warehouse
VALID_WAREHOUSE_TYPES = [
    "DISTRIBUTION",
    "FULFILLMENT",
    "COLD_STORAGE",
    "CROSS_DOCK",
    "PORT"
]

VALID_OPERATIONAL_STATUS = [
    "ACTIVE",
    "INACTIVE",
    "MAINTENANCE"
]

# inventory movements
VALID_MOVEMENT_TYPES = [
    "RECEIVED",
    "RESERVED",
    "SHIPPED",
    "RETURNED",
    "ADJUSTMENT"
]

# shipments
VALID_PRIORITIES = [
    "LOW",
    "STANDARD",
    "HIGH",
    "URGENT"
]

VALID_SHIPMENT_STATUS = [
    "REQUESTED",
    "APPROVED",
    "PICKED_UP",
    "IN_TRANSIT",
    "OUT_FOR_DELIVERY",
    "DELIVERED",
    "REJECTED"
]

# weather
VALID_WEATHER_CONDITIONS = [
    "CLEAR",
    "CLOUDY",
    "RAIN",
    "STORM",
    "SNOW",
    "FOG"
]