# Entity Model

## Overview

This document defines the core business entities of LogiFlow and the relationships between them.

The purpose of this document is to establish a common understanding of the business objects that exist within the organization before designing the data platform.

This is an **operational domain model**, not an analytical warehouse model. These entities represent the data produced by LogiFlow's operational systems.

---

# Entity Categories

The business entities are grouped into three categories:

## Master Data

Master data changes infrequently and represents core business objects.

* Customer
* Product
* Warehouse
* Carrier
* Inventory

---

## Transactional Data

Transactional entities record day-to-day business operations.

* Shipment
* ShipmentItem
* TrackingEvent
* InventoryMovement

---

## Reference Data

Reference data enriches operational data and supports analytics.

* Holiday
* Weather

---

# Entity Definitions

## Customer

### Purpose

Represents a business customer that uses LogiFlow's logistics services.

### Business Owner

Customer Management System (CMS)

### Lifecycle

Created → Updated → Deactivated

### Key Attributes

* Customer ID
* Company Name
* Industry
* Customer Tier
* Billing Address
* Contact Information
* Status

---

## Product

### Purpose

Represents products owned by customers and stored within LogiFlow warehouses.

### Business Owner

Customer Integrations Team

### Lifecycle

Created → Updated → Discontinued

### Key Attributes

* Product ID (provided by customer)
* Product Name
* Category
* Weight
* Dimensions
* Storage Type
* Hazard Classification (if applicable)

---

## Warehouse

### Purpose

Represents physical storage locations operated by LogiFlow.

### Business Owner

Warehouse Management System (WMS)

### Lifecycle

Created → Operational → Closed

### Key Attributes

* Warehouse ID
* Warehouse Name
* City
* Country
* Capacity
* Warehouse Type

---

## Carrier

### Purpose

Represents transportation partners responsible for delivering shipments.

### Business Owner

Carrier Management System

### Lifecycle

Onboarded → Active → Suspended → Retired

### Key Attributes

* Carrier ID
* Carrier Name
* Service Level
* Supported Regions
* Contract Status

---

## Inventory

### Purpose

Represents the **current available stock** of a product within a warehouse.

This entity stores the latest operational state and supports warehouse operations.

### Business Owner

Warehouse Management System (WMS)

### Lifecycle

Updated continuously as inventory changes.

### Key Attributes

* Inventory ID
* Warehouse ID
* Product ID
* Available Quantity
* Reserved Quantity
* Last Updated Timestamp

---

## Shipment

### Purpose

Represents a shipment requested by a customer.

Every shipment is created immediately and progresses through its lifecycle, even if it is later rejected.

This design enables complete operational and historical analytics.

### Business Owner

Shipment Management System (SMS)

### Lifecycle

CREATED

↓

APPROVED / REJECTED

↓

INVENTORY_RESERVED

↓

READY_FOR_PICKUP

↓

PICKED_UP

↓

IN_TRANSIT

↓

OUT_FOR_DELIVERY

↓

DELIVERED

↓

CLOSED

### Key Attributes

* Shipment ID
* Customer ID
* Origin Warehouse
* Destination
* Current Status
* Priority
* Requested Delivery Date
* Created Timestamp
* Approved Timestamp
* Delivered Timestamp
* Rejection Reason (if applicable)

---

## ShipmentItem

### Purpose

Represents an individual product included within a shipment.

A shipment may contain multiple products.

### Business Owner

Shipment Management System (SMS)

### Lifecycle

Created with Shipment

### Key Attributes

* Shipment Item ID
* Shipment ID
* Product ID
* Quantity
* Unit Weight

---

## TrackingEvent

### Purpose

Represents every operational event generated throughout a shipment's lifecycle.

This entity preserves the complete history of a shipment.

### Business Owner

Shipment Tracking Service

### Lifecycle

Append-only

### Example Events

* Shipment Created
* Shipment Approved
* Inventory Reserved
* Ready for Pickup
* Picked Up
* Arrived at Hub
* Departed Hub
* Out for Delivery
* Delivered

### Key Attributes

* Event ID
* Shipment ID
* Event Type
* Event Timestamp
* Event Location

---

## InventoryMovement

### Purpose

Represents every stock movement within the warehouse network.

Unlike Inventory, which stores the current state, InventoryMovement stores the complete historical record of inventory changes.

### Business Owner

Warehouse Management System (WMS)

### Lifecycle

Append-only

### Example Movements

* Received
* Reserved
* Released
* Transferred
* Shipped

### Key Attributes

* Movement ID
* Product ID
* Warehouse ID
* Movement Type
* Quantity
* Timestamp

---

## Holiday

### Purpose

Reference data used to explain delivery delays and improve SLA analysis.

### Business Owner

External Provider

---

## Weather

### Purpose

External weather information used to enrich transportation analytics.

### Business Owner

Weather API Provider

---

# Entity Relationships

```
Customer
    │
    └────────────── 1:N ────────────── Shipment
                                          │
                                          ├────────────── 1:N ────────────── ShipmentItem
                                          │                                   │
                                          │                                   └────────────── N:1 ────────────── Product
                                          │
                                          └────────────── 1:N ────────────── TrackingEvent

Carrier
    │
    └────────────── 1:N ────────────── Shipment

Warehouse
    │
    ├────────────── 1:N ────────────── Inventory
    │
    └────────────── 1:N ────────────── InventoryMovement

Product
    │
    ├────────────── 1:N ────────────── Inventory
    │
    └────────────── 1:N ────────────── InventoryMovement
```

---

# Design Decisions

The following architectural decisions have been made for Version 1 of the platform:

* Every shipment is created before validation.
* Rejected shipments remain in the system for historical analysis.
* A shipment may contain multiple products.
* A shipment originates from a single warehouse.
* A shipment may pass through multiple logistics hubs.
* Shipment history is stored separately from the current shipment state.
* Inventory stores the current operational state.
* InventoryMovement stores the complete historical record of inventory changes.
* TrackingEvent is an append-only event log and serves as the historical timeline for every shipment.

---

# Design Principles

The entity model follows several core principles:

1. Operational systems remain the source of truth for business entities.
2. Current operational state and historical events are modeled separately.
3. Every business entity has a clearly defined owner.
4. Historical data is preserved wherever it provides analytical value.
5. The operational model is intentionally independent of the analytical warehouse model.

---

# Relationship to the Data Platform

This entity model defines the operational business objects that will be ingested into the Bronze layer of the data platform.

Subsequent stages of the platform will standardize, validate, transform, and model these entities into analytics-ready datasets, culminating in a dimensional warehouse and Gold-layer business metrics.
