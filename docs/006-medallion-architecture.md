# Medallion Architecture

## Overview

This document describes the Medallion Architecture adopted by the LogiFlow Analytics Platform.

The Medallion Architecture organizes data into progressive quality layers, allowing raw operational data to evolve into trusted analytical datasets and business-ready insights.

Each layer has a single responsibility and serves a different group of consumers within the organization.

---

# Objectives

The Medallion Architecture is designed to achieve the following goals:

* Preserve original operational data.
* Build trusted datasets through incremental refinement.
* Separate operational processing from analytical modeling.
* Support reproducible and auditable pipelines.
* Enable future batch and streaming processing using the same architecture.

---

# Layer Overview

```text
Operational Systems
        │
        ▼
Ingestion Layer
        │
        ▼
Bronze
        │
   (Spark Processing)
        ▼
Silver
        │
   (Spark Processing)
        ▼
Analytics Warehouse
        │
   (Spark Processing)
        ▼
Gold
        │
        ▼
Business Users
```

---

# Bronze Layer

## Purpose

The Bronze layer stores data exactly as it is received from operational systems.

It represents the immutable landing zone of the data platform.

No business transformations are performed in this layer.

The objective is to preserve complete source fidelity and allow pipelines to be replayed whenever necessary.

---

## Characteristics

* Raw source data
* Immutable
* Source-oriented
* Supports replay
* Supports debugging
* No business logic

---

## Storage Format

Bronze preserves the original source format.

Examples:

* REST API responses → JSON
* CSV exports → CSV

No conversion to Parquet is performed in Bronze.

---

## Folder Structure

```text
bronze/

    customer/
    warehouse/
    shipment/
    tracking/
    carrier/
    weather/
    holiday/
```

---

## Consumers

Primary consumers include:

* Data Engineers
* Pipeline developers

---

# Silver Layer

## Purpose

The Silver layer transforms raw operational data into trusted datasets suitable for downstream processing.

This layer represents the operational source of truth for the data platform.

---

## Typical Transformations

* Schema standardization
* Duplicate removal
* Null handling
* Timestamp normalization
* Data validation
* Basic enrichment
* Standardized naming conventions

---

## Characteristics

* Clean
* Validated
* Standardized
* Query efficient
* Operationally trusted

---

## Storage Format

Apache Parquet

---

## Folder Structure

```text
silver/

    customer/
    warehouse/
    shipment/
    tracking/
    carrier/
    inventory/
```

---

## Consumers

* Data Engineers
* Data Analysts
* Downstream ETL pipelines

---

# Analytics Warehouse

## Purpose

The Analytics Warehouse reorganizes operational entities into analytical models optimized for reporting and historical analysis.

Unlike the Silver layer, which mirrors operational systems, the warehouse models business facts and dimensions.

---

## Characteristics

* Dimensional modeling
* Historical analysis
* Star schema
* Reusable analytical foundation

---

## Structure

```text
warehouse/

    dimensions/

        dim_customer
        dim_product
        dim_carrier
        dim_warehouse
        dim_date

    facts/

        fact_shipment
        fact_shipment_item
        fact_tracking_event
```

---

## Storage Format

Apache Parquet

---

## Consumers

* Data Analysts
* Data Scientists
* BI Developers

---

# Gold Layer

## Purpose

The Gold layer contains business-ready datasets specifically created for reporting, dashboards, and executive decision-making.

These datasets are curated products rather than reusable analytical models.

---

## Examples

* Daily Shipment KPI
* Carrier Performance
* Warehouse Utilization
* On-Time Delivery
* SLA Compliance
* Executive Dashboard

---

## Characteristics

* Business-oriented
* Aggregated
* Curated
* Dashboard-ready

---

## Structure

```text
gold/

    kpis/

        daily_shipment_kpi
        carrier_performance
        warehouse_utilization
        sla_summary

    dashboards/

        executive_dashboard
```

---

## Storage Format

Apache Parquet

---

## Consumers

* Executives
* Business Users
* Dashboard Applications

---

# Supporting Layers

## Quarantine

Records that fail validation are moved into the Quarantine layer.

No records are silently discarded.

Examples include:

* Missing mandatory fields
* Invalid timestamps
* Invalid identifiers
* Schema violations

```text
quarantine/

    shipment/
    tracking/
```

---

## Metadata

Operational metadata supporting the platform is stored separately from business data.

Examples include:

* Pipeline execution history
* Record counts
* Schema versions
* Audit information

```text
metadata/

    audit/
    pipeline_runs/
    schema_versions/
```

---

# Physical Data Lake Structure

The platform uses a single Amazon S3 bucket containing all logical layers.

```text
logiflow-data-platform/

├── bronze/
│
├── silver/
│
├── warehouse/
│
├── gold/
│
├── quarantine/
│
└── metadata/
```

Each layer is further organized by business domain where appropriate.

---

# Partitioning Strategy

Partitioning is applied only to large, append-heavy datasets.

| Entity            | Partition Strategy |
| ----------------- | ------------------ |
| Shipment          | Created Date       |
| TrackingEvent     | Event Date         |
| InventoryMovement | Movement Date      |
| Weather           | Observation Date   |

Small reference and master datasets such as Customer, Carrier, Holiday, and Warehouse remain unpartitioned unless future scale requires otherwise.

---

# Data Flow

```text
Operational Systems
        │
        ▼
Ingestion
        │
        ▼
Bronze
        │
        ▼
Silver
        │
        ▼
Analytics Warehouse
        │
        ▼
Gold
```

Each downstream layer depends only on the immediately preceding layer, simplifying lineage, testing, and recovery.

---

# Design Principles

The Medallion Architecture follows these principles:

1. Every layer has a single responsibility.
2. Original source data is never overwritten.
3. Transformations are incremental and traceable.
4. Current operational state is separated from historical events.
5. Business-ready datasets are derived from reusable analytical models.
6. Data quality issues are isolated rather than silently ignored.
7. The architecture is designed to support both batch and future streaming workloads.

---

# Future Evolution

The architecture is intentionally designed for incremental evolution.

Future enhancements include:

* Streaming ingestion
* Kafka integration
* Spark Structured Streaming
* Automated data quality checks
* Data observability
* Cost optimization
* Schema evolution handling

These capabilities can be introduced without changing the overall Medallion Architecture.

---

# Relationship to the Platform

The Medallion Architecture defines how operational data progresses through the LogiFlow Analytics Platform.

Combined with the Business Domain, Source Systems, Business Process, Entity Model, and Data Platform Architecture documents, it provides the complete architectural blueprint for implementation.

The next phase of the project focuses on implementing this architecture using AWS services, Apache Spark, and Apache Airflow.
