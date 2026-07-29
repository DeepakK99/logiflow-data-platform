# Source Data Model

## Overview

This document defines the operational datasets produced by each source system within LogiFlow.

Unlike the Entity Model, which describes business concepts, the Source Data Model defines the physical datasets exported by operational systems for ingestion into the analytics platform.

These datasets serve as the input to the Bronze layer of the Medallion Architecture.

---

# Design Principles

The source data model follows these principles:

* Each operational system owns its own data.
* Source schemas remain independent.
* Data reflects operational reality, not analytical requirements.
* Relationships are maintained through business identifiers.
* Schemas are versionable and may evolve over time.

---

# Customer Management System (CMS)

## Dataset: customers

### Description

Stores business customers using LogiFlow's logistics services.

| Column          | Type      | Description                |
| --------------- | --------- | -------------------------- |
| customer_id     | UUID      | Unique customer identifier |
| company_name    | STRING    | Customer company name      |
| industry        | STRING    | Industry sector            |
| customer_tier   | STRING    | Bronze / Silver / Gold     |
| billing_country | STRING    | Headquarters country       |
| contact_email   | STRING    | Primary business contact   |
| account_status  | STRING    | ACTIVE / INACTIVE          |
| created_at      | TIMESTAMP | Customer creation time     |
| updated_at      | TIMESTAMP | Last modification          |

---

# Product Management System

## Dataset: products

### Description

Stores products owned by customers.

| Column         | Type      | Description                |
| -------------- | --------- | -------------------------- |
| product_id     | UUID      | Product identifier         |
| customer_id    | UUID      | Owning customer            |
| sku            | STRING    | Customer SKU               |
| product_name   | STRING    | Product name               |
| category       | STRING    | Product category           |
| weight_kg      | DECIMAL   | Weight                     |
| length_cm      | DECIMAL   | Length                     |
| width_cm       | DECIMAL   | Width                      |
| height_cm      | DECIMAL   | Height                     |
| storage_type   | STRING    | Ambient / Chilled / Frozen |
| hazardous_flag | BOOLEAN   | Hazardous goods indicator  |
| created_at     | TIMESTAMP | Creation timestamp         |
| updated_at     | TIMESTAMP | Last modification          |

---

# Warehouse Management System (WMS)

## Dataset: warehouses

### Description

Represents physical warehouses operated by LogiFlow.

| Column             | Type      | Description                          |
| ------------------ | --------- | ------------------------------------ |
| warehouse_id       | UUID      | Warehouse identifier                 |
| warehouse_name     | STRING    | Warehouse name                       |
| city               | STRING    | City                                 |
| country            | STRING    | Country                              |
| warehouse_type     | STRING    | Regional / Distribution / Fulfilment |
| storage_capacity   | INTEGER   | Maximum pallet capacity              |
| operational_status | STRING    | ACTIVE / MAINTENANCE / CLOSED        |
| created_at         | TIMESTAMP | Creation timestamp                   |

---

## Dataset: inventory

### Description

Current inventory snapshot for each product in each warehouse.

| Column             | Type      | Description        |
| ------------------ | --------- | ------------------ |
| inventory_id       | UUID      | Inventory record   |
| warehouse_id       | UUID      | Warehouse          |
| product_id         | UUID      | Product            |
| available_quantity | INTEGER   | Available stock    |
| reserved_quantity  | INTEGER   | Reserved stock     |
| last_updated       | TIMESTAMP | Snapshot timestamp |

---

## Dataset: inventory_movements

### Description

Historical inventory transactions.

| Column             | Type      | Description                                            |
| ------------------ | --------- | ------------------------------------------------------ |
| movement_id        | UUID      | Movement identifier                                    |
| warehouse_id       | UUID      | Warehouse                                              |
| product_id         | UUID      | Product                                                |
| movement_type      | STRING    | RECEIVED / RESERVED / RELEASED / SHIPPED / TRANSFERRED |
| quantity           | INTEGER   | Quantity moved                                         |
| movement_timestamp | TIMESTAMP | Event timestamp                                        |

---

# Shipment Management System (SMS)

## Dataset: shipments

### Description

Shipment requests created by customers.

| Column                  | Type      | Description             |
| ----------------------- | --------- | ----------------------- |
| shipment_id             | UUID      | Shipment identifier     |
| customer_id             | UUID      | Customer                |
| origin_warehouse_id     | UUID      | Origin warehouse        |
| destination_country     | STRING    | Delivery country        |
| destination_city        | STRING    | Delivery city           |
| priority                | STRING    | STANDARD / EXPRESS      |
| shipment_status         | STRING    | Current shipment status |
| requested_delivery_date | DATE      | Requested delivery      |
| approved_at             | TIMESTAMP | Approval timestamp      |
| delivered_at            | TIMESTAMP | Delivery timestamp      |
| rejection_reason        | STRING    | Reason if rejected      |
| created_at              | TIMESTAMP | Creation timestamp      |

---

## Dataset: shipment_items

### Description

Products contained within shipments.

| Column           | Type    | Description    |
| ---------------- | ------- | -------------- |
| shipment_item_id | UUID    | Shipment item  |
| shipment_id      | UUID    | Shipment       |
| product_id       | UUID    | Product        |
| quantity         | INTEGER | Quantity       |
| unit_weight      | DECIMAL | Product weight |

---

# Carrier Management System

## Dataset: carriers

### Description

Transportation partners.

| Column            | Type   | Description        |
| ----------------- | ------ | ------------------ |
| carrier_id        | UUID   | Carrier identifier |
| carrier_name      | STRING | Carrier name       |
| service_level     | STRING | Standard / Express |
| supported_regions | STRING | Service regions    |
| contract_status   | STRING | ACTIVE / SUSPENDED |

---

# Shipment Tracking Service

## Dataset: tracking_events

### Description

Append-only shipment event log.

| Column          | Type      | Description                 |
| --------------- | --------- | --------------------------- |
| event_id        | UUID      | Event identifier            |
| shipment_id     | UUID      | Shipment                    |
| carrier_id      | UUID      | Carrier                     |
| event_type      | STRING    | Shipment lifecycle event    |
| warehouse_id    | UUID      | Warehouse or hub (nullable) |
| event_city      | STRING    | Event location              |
| event_country   | STRING    | Event country               |
| event_timestamp | TIMESTAMP | Event time                  |

---

# Weather Service

## Dataset: weather

### Description

Daily weather observations for logistics locations.

| Column            | Type    | Description                 |
| ----------------- | ------- | --------------------------- |
| weather_id        | UUID    | Observation identifier      |
| observation_date  | DATE    | Observation date            |
| city              | STRING  | City                        |
| country           | STRING  | Country                     |
| temperature_c     | DECIMAL | Temperature                 |
| precipitation_mm  | DECIMAL | Rainfall                    |
| weather_condition | STRING  | Sunny / Rain / Snow / Storm |

---

# Holiday Calendar

## Dataset: holidays

### Description

Public holiday reference data.

| Column       | Type   | Description        |
| ------------ | ------ | ------------------ |
| holiday_id   | UUID   | Holiday identifier |
| country      | STRING | Country            |
| holiday_name | STRING | Holiday name       |
| holiday_date | DATE   | Holiday date       |

---

# Data Ownership

| Dataset             | Source System               |
| ------------------- | --------------------------- |
| customers           | Customer Management System  |
| products            | Product Management System   |
| warehouses          | Warehouse Management System |
| inventory           | Warehouse Management System |
| inventory_movements | Warehouse Management System |
| shipments           | Shipment Management System  |
| shipment_items      | Shipment Management System  |
| carriers            | Carrier Management System   |
| tracking_events     | Shipment Tracking Service   |
| weather             | External Weather API        |
| holidays            | Holiday Calendar API        |

---

# Source Relationships

```text
customers
    │
    └──────< products

customers
    │
    └──────< shipments
                   │
                   └──────< shipment_items
                                  │
                                  └────── products

warehouses
    │
    ├──────< inventory
    │
    ├──────< inventory_movements
    │
    └──────< shipments

shipments
    │
    └──────< tracking_events

carriers
    │
    └──────< tracking_events
```

---

# Expected Data Volumes

| Dataset             | Frequency       | Estimated Daily Volume |
| ------------------- | --------------- | ---------------------: |
| customers           | Occasional      |            <10 changes |
| products            | Occasional      |            <20 changes |
| warehouses          | Rare            |             <5 changes |
| inventory           | Hourly Snapshot |         ~4,000 records |
| inventory_movements | Continuous      |         ~1,500 records |
| shipments           | Daily           |           ~300 records |
| shipment_items      | Daily           |           ~900 records |
| tracking_events     | Continuous      |         ~2,500 records |
| weather             | Daily           |           ~100 records |
| holidays            | Annual          |                Minimal |

---

# Relationship to the Data Platform

These operational datasets are generated by LogiFlow's source systems and ingested into the Bronze layer without modification.

Subsequent processing stages will validate, standardize, enrich, and transform these datasets into trusted operational data (Silver), analytical models (Warehouse), and business-ready datasets (Gold).
