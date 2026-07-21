# Source Systems

## Overview

LogiFlow operates several independent operational systems, each responsible for a specific business capability.

These systems are optimized for day-to-day business operations (OLTP) rather than analytics. The purpose of the data platform is to consolidate data from these systems into a centralized analytics platform.

Each source system has:

* A business owner
* A primary responsibility
* Data entities it owns
* A publishing frequency
* A preferred ingestion mechanism

---

# Source System 1 — Customer Management System (CMS)

## Business Owner

Customer Operations Team

## Purpose

Maintains information about all business customers using LogiFlow's logistics services.

## Data Produced

* Customers
* Customer addresses
* Customer contacts
* Billing information
* Customer status

## Example Entities

* Customer
* CustomerAddress

## Update Frequency

Daily

## Ingestion Method

Daily CSV export (simulating a legacy enterprise application)

---

# Source System 2 — Warehouse Management System (WMS)

## Business Owner

Warehouse Operations Team

## Purpose

Manages inventory stored in LogiFlow warehouses.

Tracks product movement inside warehouses and inventory availability.

## Data Produced

* Warehouses
* Inventory
* Stock movements
* Warehouse capacity
* Storage locations

## Example Entities

* Warehouse
* Inventory
* InventoryMovement

## Update Frequency

Hourly

## Ingestion Method

REST API

---

# Source System 3 — Shipment Management System (SMS)

## Business Owner

Shipment Operations Team

## Purpose

Creates and manages shipments requested by customers.

Responsible for shipment planning before transportation begins.

## Data Produced

* Shipments
* Shipment Items
* Shipping Requests
* Shipment Status

## Example Entities

* Shipment
* ShipmentItem

## Update Frequency

Hourly

## Ingestion Method

REST API

---

# Source System 4 — Transportation Management System (TMS)

## Business Owner

Transportation Operations Team

## Purpose

Plans and manages transportation between warehouses and delivery destinations.

Responsible for assigning carriers and optimizing routes.

## Data Produced

* Routes
* Carrier assignments
* Vehicles
* Transportation schedules

## Example Entities

* Route
* CarrierAssignment
* Vehicle

## Update Frequency

Every 4 hours

## Ingestion Method

REST API

---

# Source System 5 — Shipment Tracking Service

## Business Owner

Tracking Team

## Purpose

Records every operational event occurring during shipment delivery.

This system represents the operational timeline of each shipment.

## Data Produced

* Shipment events
* Tracking status
* Event timestamps
* Event locations

## Example Entities

* TrackingEvent

## Example Events

* Shipment Created
* Carrier Assigned
* Picked Up
* Arrived at Warehouse
* Departed Warehouse
* In Transit
* Out for Delivery
* Delivered

## Update Frequency

Near Real-Time

## Ingestion Method

REST API (Batch in Phase 1, Streaming in a future phase)

---

# Source System 6 — Carrier Management System

## Business Owner

Carrier Partnership Team

## Purpose

Maintains information about logistics partners responsible for transportation.

## Data Produced

* Carriers
* Carrier contracts
* Service levels
* Carrier regions

## Example Entities

* Carrier

## Update Frequency

Weekly

## Ingestion Method

CSV export

---

# Source System 7 — Product Catalog

## Business Owner

Customer Integrations Team

## Purpose

Maintains product information supplied by LogiFlow customers.

Product ownership remains with customers, while LogiFlow stores product metadata required for warehousing and shipment.

## Data Produced

* Products
* Product categories
* Product dimensions
* Product weight

## Example Entities

* Product

## Update Frequency

Daily

## Ingestion Method

CSV upload

---

# External Source 1 — Holiday Calendar

## Business Owner

External Provider

## Purpose

Provides national and regional holidays used to explain delivery delays and calculate expected delivery dates.

## Update Frequency

Monthly

## Ingestion Method

CSV download

---

# External Source 2 — Weather Data

## Business Owner

External Weather API

## Purpose

Provides weather conditions that may influence transportation and delivery performance.

## Data Produced

* Temperature
* Rainfall
* Weather conditions
* Wind speed

## Update Frequency

Hourly

## Ingestion Method

REST API

---

# Summary

| Source System                    | Primary Data          | Frequency      | Ingestion                  |
| -------------------------------- | --------------------- | -------------- | -------------------------- |
| Customer Management System       | Customers             | Daily          | CSV                        |
| Warehouse Management System      | Warehouses, Inventory | Hourly         | REST API                   |
| Shipment Management System       | Shipments             | Hourly         | REST API                   |
| Transportation Management System | Routes, Vehicles      | Every 4 Hours  | REST API                   |
| Shipment Tracking Service        | Shipment Events       | Near Real-Time | REST API (Streaming later) |
| Carrier Management System        | Carriers              | Weekly         | CSV                        |
| Product Catalog                  | Products              | Daily          | CSV                        |
| Holiday Calendar                 | Holidays              | Monthly        | CSV                        |
| Weather API                      | Weather               | Hourly         | REST API                   |

## sample data flow
```text
Customer Places Shipping Request
            ↓
    Shipment Created
            ↓
    Inventory Reserved
            ↓
    Carrier Assigned
            ↓
    Shipment Picked Up
            ↓
   Warehouse Transfers
            ↓
        Delivered
```