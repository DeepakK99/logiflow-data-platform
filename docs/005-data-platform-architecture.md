# Data Platform Architecture

## Overview

This document describes the logical architecture of the LogiFlow Analytics Platform.

The objective of the platform is to collect operational data from multiple business systems, transform it into trusted analytical datasets, and deliver business-ready insights for reporting and decision-making.

The architecture is designed using a layered approach where each layer has a single responsibility.

---

# Architecture Principles

The platform follows the following design principles:

* Single responsibility for every layer.
* Preserve original source data.
* Separate operational data from analytical data.
* Build reusable datasets before creating business KPIs.
* Keep ingestion independent of data transformation.
* Design for future scalability and streaming support.

---

# High-Level Architecture

```text
                           Operational Systems
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│ CMS │ WMS │ SMS │ Tracking │ Carrier │ Weather │ Holiday    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
                     Ingestion Layer
                             │
                             ▼
                        Bronze Layer
                             │
                      (Spark Processing)
                             ▼
                        Silver Layer
                             │
                      (Spark Processing)
                             ▼
                  Analytics Warehouse
                             │
                      (Spark Processing)
                             ▼
                         Gold Layer
                             │
         ┌───────────────────┴───────────────────┐
         ▼                                       ▼
      Amazon Athena                     BI / Dashboards
```

---

# Platform Layers

## 1. Operational Systems

### Purpose

Operational systems execute LogiFlow's day-to-day business processes.

These systems are the source of truth for business operations and are owned by different business teams.

Examples include:

* Customer Management System
* Warehouse Management System
* Shipment Management System
* Shipment Tracking Service
* Carrier Management System
* External Weather API
* Holiday Calendar

The analytics platform does **not** modify these systems.

---

## 2. Ingestion Layer

### Purpose

The ingestion layer is responsible for moving data from operational systems into the platform.

Responsibilities include:

* Reading APIs
* Reading CSV files
* Basic file validation
* Capturing ingestion metadata
* Writing raw data to the Bronze layer

The ingestion layer performs **no business transformations**.

---

## 3. Bronze Layer

### Purpose

The Bronze layer preserves the original data exactly as it was received from each source system.

This layer acts as the immutable historical archive of operational data.

Characteristics:

* Raw source data
* No business transformations
* Supports replay and debugging
* Source-oriented organization

Typical folder structure:

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

Bronze is intended primarily for Data Engineers.

---

## 4. Silver Layer

### Purpose

The Silver layer contains trusted operational data.

Data in this layer has been cleaned, validated, standardized, and enriched while still preserving the operational business model.

Typical transformations include:

* Schema standardization
* Duplicate removal
* Data quality validation
* Standardized timestamps
* Consistent naming conventions

Silver represents the trusted operational dataset used by downstream analytical processes.

Primary consumers:

* Data Engineers
* Advanced Analysts

---

## 5. Analytics Warehouse

### Purpose

The Analytics Warehouse reorganizes operational data into an analytical model optimized for reporting and ad-hoc analysis.

Unlike the Silver layer, which mirrors operational entities, the warehouse is designed around analytical concepts.

Examples include:

* Fact tables
* Dimension tables
* Historical snapshots

This layer provides a reusable analytical foundation for multiple business use cases.

Primary consumers:

* Data Analysts
* Data Scientists

---

## 6. Gold Layer

### Purpose

The Gold layer contains business-ready datasets created for specific reporting and dashboard requirements.

Rather than exposing raw analytical models, the Gold layer provides curated outputs that directly answer business questions.

Examples include:

* Daily Shipment KPIs
* Carrier Performance
* Warehouse Utilization
* SLA Compliance
* Executive Operational Dashboard

Primary consumers:

* Business Users
* Executives
* BI Dashboards

---

# Processing Engine

The platform uses Apache Spark as its distributed processing engine.

Spark is **not** a storage layer.

Instead, Spark performs transformations between layers.

Examples include:

* Bronze → Silver
* Silver → Warehouse
* Warehouse → Gold

Separating processing from storage allows each layer to remain independent and reusable.

---

# Orchestration

Apache Airflow orchestrates the execution of the platform.

Airflow is responsible for:

* Scheduling pipelines
* Managing dependencies
* Handling retries
* Monitoring workflow execution

Airflow coordinates the platform but does not perform data transformations.

---

# Storage

Amazon S3 serves as the storage layer for the platform.

S3 stores datasets for all logical layers:

* Bronze
* Silver
* Analytics Warehouse
* Gold

Each layer remains physically separated within the data lake.

---

# Metadata Management

AWS Glue Data Catalog stores metadata describing datasets within the platform.

The catalog maintains:

* Dataset locations
* Schemas
* Partitions
* Table definitions

The catalog enables analytical services to discover and query datasets stored in Amazon S3.

---

# Query Layer

Amazon Athena provides serverless SQL access to datasets registered in the Glue Data Catalog.

Typical usage includes:

Business Users

* Query Gold datasets.

Data Analysts

* Query warehouse tables.

Data Engineers

* Validate Silver datasets during development and troubleshooting.

---

# Consumer View

| Layer               | Primary Consumer                       |
| ------------------- | -------------------------------------- |
| Bronze              | Data Engineers                         |
| Silver              | Data Engineers, Advanced Analysts      |
| Analytics Warehouse | Data Analysts, Data Scientists         |
| Gold                | Business Users, Dashboards, Executives |

---

# Responsibilities by Layer

| Layer               | Primary Responsibility              |
| ------------------- | ----------------------------------- |
| Operational Systems | Execute business operations         |
| Ingestion           | Move data into the platform         |
| Bronze              | Preserve original data              |
| Silver              | Create trusted operational datasets |
| Analytics Warehouse | Build reusable analytical models    |
| Gold                | Deliver business-ready datasets     |

---

# Future Evolution

The architecture is intentionally designed to evolve over time.

Future enhancements may include:

* Streaming ingestion
* Event-driven processing
* Real-time analytics
* Data quality monitoring
* Advanced observability
* Cost optimization
* Multi-cloud deployments

The layered architecture allows these capabilities to be introduced incrementally without fundamental changes to the platform design.

---

# Relationship to the Project

This document defines the logical architecture of the LogiFlow Analytics Platform.

Subsequent documents will describe:

* Medallion architecture implementation
* AWS infrastructure
* Data modeling
* Orchestration
* Streaming evolution

This architecture serves as the blueprint for all implementation work performed throughout the project.
