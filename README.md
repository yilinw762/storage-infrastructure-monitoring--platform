# storage-infrastructure-monitoring-platform

# Storage Infrastructure Monitoring Platform

## Overview

The **Storage Infrastructure Monitoring Platform** is a full-stack infrastructure engineering project that simulates a real-world enterprise storage monitoring and automation system. The platform collects storage device metrics through APIs, validates incoming data, stores it in a PostgreSQL database, and provides reporting and visualization capabilities through a web dashboard.

This project is inspired by modern storage engineering environments where infrastructure teams manage thousands of storage devices and rely heavily on automation, APIs, databases, testing, and analytics to maintain reliability and operational efficiency.

---

## Architecture

```text
┌─────────────────────┐
│ Storage Devices     │
│ (Simulated APIs)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ API Gateway / Proxy │
│ (Apigee Simulation) │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Python Collector    │
│ Data Collection     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Validation Engine   │
│ Data Quality Checks │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ PostgreSQL Database │
│ Metrics Repository  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Reporting Layer     │
│ SQL Analytics       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Dashboard UI        │
│ Monitoring Portal   │
└─────────────────────┘
```

---

# Features

## Storage Device API

Simulates enterprise storage systems by exposing REST APIs for:

* Storage device inventory
* Capacity metrics
* Performance metrics
* Health status
* Latency measurements
* IOPS statistics

### Example Endpoint

```http
GET /devices
```

Response:

```json
[
  {
    "device_id": "dev001",
    "hostname": "storage-east-01",
    "location": "East Data Center",
    "capacity_tb": 500
  }
]
```

---

## API Gateway Simulation

Simulates an API management platform such as Apigee.

Features:

* API authentication
* Request forwarding
* Access control
* Logging
* Centralized API management

### Example Flow

```text
Client
  ↓
API Gateway
  ↓
Storage Service
```

---

## Automated Data Collection

Python automation jobs periodically collect metrics from storage APIs.

Collected data includes:

* Capacity utilization
* Latency
* Throughput
* IOPS
* Health status

Example:

```python
response = requests.get(
    "http://localhost:8000/metrics"
)

metrics = response.json()
```

---

## Data Validation Engine

Validates incoming metrics before insertion into the database.

Checks include:

### Capacity Validation

```python
if capacity_tb < 0:
    raise ValidationError
```

### Utilization Validation

```python
if used_tb > capacity_tb:
    raise ValidationError
```

### Latency Validation

```python
if latency_ms < 0:
    raise ValidationError
```

### Health Status Validation

```python
if health_status not in valid_states:
    raise ValidationError
```

---

## PostgreSQL Data Warehouse

Stores all device metadata and collected metrics.

### Devices Table

```sql
CREATE TABLE devices (
    device_id TEXT PRIMARY KEY,
    hostname TEXT,
    location TEXT,
    vendor TEXT
);
```

### Metrics Table

```sql
CREATE TABLE metrics (
    id SERIAL PRIMARY KEY,
    device_id TEXT,
    used_tb NUMERIC,
    capacity_tb NUMERIC,
    latency_ms NUMERIC,
    iops INTEGER,
    collected_at TIMESTAMP
);
```

---

## Analytics & Reporting

Generate operational reports using SQL.

### Devices Above 90% Capacity

```sql
SELECT *
FROM metrics
WHERE used_tb / capacity_tb > 0.9;
```

### Average Storage Utilization

```sql
SELECT AVG(
    used_tb / capacity_tb
)
FROM metrics;
```

### Capacity by Data Center

```sql
SELECT
    location,
    SUM(capacity_tb)
FROM devices
GROUP BY location;
```

---

## Automated Testing

Comprehensive testing suite built with pytest.

### API Testing

```python
def test_api_returns_200():
```

### Validation Testing

```python
def test_negative_capacity():
```

### Data Integrity Testing

```python
def test_utilization_not_exceed_capacity():
```

### Database Testing

```python
def test_metrics_insert_successfully():
```

---

## Dashboard

Web dashboard displaying:

### Device Inventory

| Device | Location | Capacity |
| ------ | -------- | -------- |

### Utilization Monitoring

| Device | Used | Capacity | Utilization |
| ------ | ---- | -------- | ----------- |

### Health Status

* Healthy
* Warning
* Critical

### Analytics

* Average utilization
* Device count
* Capacity forecasts
* Alert summaries

---

# Technology Stack

## Backend

* Python 3.12
* FastAPI
* Requests

## Database

* PostgreSQL
* YugabyteDB Compatible SQL

## Frontend

* HTML
* Bootstrap
* JavaScript

## Testing

* Pytest

## Infrastructure

* Docker
* Docker Compose

## API Management

* Apigee-style API Gateway Simulation

## Version Control

* Git
* GitHub

---

# Project Structure

```text
storage-monitoring-platform/

├── api/
│   ├── devices.py
│   ├── metrics.py
│   └── gateway.py
│
├── collector/
│   ├── collector.py
│   └── scheduler.py
│
├── validation/
│   └── validators.py
│
├── database/
│   ├── models.py
│   └── repository.py
│
├── reports/
│   ├── utilization.py
│   └── analytics.py
│
├── dashboard/
│   ├── templates/
│   ├── static/
│   └── app.py
│
├── tests/
│   ├── test_api.py
│   ├── test_validation.py
│   └── test_database.py
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# Learning Objectives

This project demonstrates:

### Software Engineering

* REST API development
* Backend architecture
* Modular design

### Database Engineering

* PostgreSQL
* SQL queries
* Indexing
* Data modeling

### Infrastructure Engineering

* Storage monitoring concepts
* Capacity planning
* Operational reporting

### Automation

* Data collection pipelines
* Validation workflows
* Scheduled jobs

### Testing

* Unit testing
* API testing
* Data validation testing

### Enterprise Concepts

* API gateways
* Authentication
* Data governance
* Monitoring systems

---

# Future Enhancements

* OAuth authentication
* Role-based access control
* Grafana dashboards
* Kubernetes deployment
* Kafka event streaming
* Prometheus metrics collection
* Distributed database support (YugabyteDB cluster)
* CI/CD pipelines with GitHub Actions

