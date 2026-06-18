# Secure IoT Monitoring Platform

**Created by HAMAILI Ahmed-Imad**

A secure and containerized IoT monitoring platform for collecting, storing, visualizing and analyzing telemetry from connected devices.

This project demonstrates a realistic end-to-end IoT architecture built around MQTT, FastAPI, PostgreSQL, Docker, Prometheus, Grafana and a Vue dashboard. It is designed to show how networked systems, backend engineering, cybersecurity, DevOps, observability and embedded IoT concepts can work together in one complete platform.

## Project purpose

Most IoT demos stop at sending random sensor values to a dashboard. This project goes further by adding the components that are usually expected in a professional platform:

- registered devices with API keys
- telemetry ingestion over MQTT
- backend validation before storage
- anomaly detection rules
- REST APIs for dashboards and integrations
- PostgreSQL persistence
- Prometheus-compatible metrics
- Grafana dashboard provisioning
- Docker Compose deployment
- a clean Vue interface for monitoring
- technical documentation explaining the architecture and code flow

The current version is intentionally simple enough to run locally, but the repository is structured like a real platform so it can be extended step by step.

## Architecture

```txt
IoT Device Simulator
        |
        | MQTT telemetry
        v
Eclipse Mosquitto Broker
        |
        | MQTT subscription
        v
FastAPI Ingestion Backend
        |
        | validated SQL writes
        v
PostgreSQL Database
        |
        | REST API
        v
Vue Monitoring Dashboard

FastAPI Backend
        |
        | /metrics
        v
Prometheus
        |
        | datasource
        v
Grafana Dashboard
```

## Tech stack

| Area | Tools |
| --- | --- |
| IoT messaging | MQTT, Eclipse Mosquitto |
| Backend | Python, FastAPI, SQLAlchemy |
| Database | PostgreSQL |
| Frontend | Vue 3, TypeScript, Bootstrap 5 |
| Observability | Prometheus, Grafana, FastAPI metrics |
| DevOps | Docker Compose, GitHub Actions |
| Security | Device API keys, payload validation, isolated services |

## Features

- Simulated ESP32/Raspberry Pi/industrial sensors
- MQTT telemetry ingestion
- Device registry with hashed API keys
- Measurement storage in PostgreSQL
- Latest measurements endpoint
- Per-device measurement history
- Alert generation for abnormal values
- System summary endpoint
- Prometheus metrics endpoint
- Provisioned Grafana monitoring dashboard
- Responsive Vue dashboard
- Dockerized local environment

## Quick start

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/secure-iot-monitoring-platform.git
cd secure-iot-monitoring-platform
```

### 2. Start the platform

```bash
docker compose up --build
```

### 3. Open the services

| Service | URL |
| --- | --- |
| Vue dashboard | http://localhost:5173 |
| FastAPI docs | http://localhost:8000/docs |
| API health | http://localhost:8000/health |
| Prometheus metrics | http://localhost:8000/metrics |
| Prometheus UI | http://localhost:9090 |
| Grafana dashboard | http://localhost:3001 |

## Grafana access

Default Grafana credentials for local development:

| Field | Value |
| --- | --- |
| URL | http://localhost:3001 |
| Username | `admin` |
| Password | `admin` |

The default dashboard is available in:

```txt
Dashboards > Secure IoT Monitoring > Secure IoT Monitoring Overview
```

## Default simulated devices

The simulator publishes telemetry for the following devices:

| Device ID | Demo key |
| --- | --- |
| `esp32-room-01` | `room-01-demo-key` |
| `esp32-room-02` | `room-02-demo-key` |
| `raspberry-lab-01` | `raspberry-lab-demo-key` |
| `industrial-sensor-01` | `industrial-sensor-demo-key` |

In a real deployment, these keys would be generated per device, rotated regularly and stored outside the repository.

## Example MQTT payload

```json
{
  "device_id": "esp32-room-01",
  "device_key": "room-01-demo-key",
  "temperature": 24.7,
  "humidity": 51.3,
  "battery": 87.5,
  "rssi": -62,
  "status": "online",
  "timestamp": "2026-06-17T12:00:00Z"
}
```

## API endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/health` | Service and database health |
| GET | `/devices` | List registered devices |
| POST | `/devices` | Register a new device |
| GET | `/measurements/latest` | Latest telemetry values |
| GET | `/measurements/devices/{device_id}` | Telemetry history for one device |
| GET | `/alerts` | Generated alerts |
| GET | `/stats/summary` | Platform summary |
| GET | `/metrics` | Prometheus metrics |

## Repository structure

```txt
secure-iot-monitoring-platform/
├── backend/              # FastAPI application
├── frontend/             # Vue 3 dashboard
├── iot-simulator/        # MQTT telemetry generator
├── mqtt/                 # Mosquitto configuration
├── monitoring/           # Prometheus and Grafana configuration
├── docs/                 # Architecture, security and technical notes
├── docker-compose.yml
└── README.md
```

## Documentation

The `docs/` folder contains extra explanations:

- `architecture.md` explains the service responsibilities and data flow.
- `security.md` explains the current security model and production hardening ideas.
- `roadmap.md` shows the next planned improvements.
- `technical-documentation.md` explains the code structure, main functions and extension points.

## Development commands

```bash
# Start everything
docker compose up --build

# Stop services
docker compose down

# Stop and remove database/Grafana volumes
docker compose down -v

# Run backend tests locally from backend/
pytest
```

## Notes about comments

The code contains English comments and docstrings explaining the main design decisions, functions and service responsibilities. JSON files are intentionally kept as valid JSON, because standard JSON does not support comments.

## Project goal

The goal of this project is to demonstrate how secure networked systems can be designed across IoT, cloud infrastructure, distributed architecture, cybersecurity, DevOps and AI-ready monitoring.
