# Architecture Notes

**Author: HAMAILI Ahmed-Imad**

This platform is split into small services so each technical responsibility stays clear and easy to review.

## Components

### IoT simulator

The simulator behaves like a small fleet of connected devices. It publishes telemetry to MQTT topics using the following convention:

```txt
iot/{device_id}/telemetry
```

Each message contains a device identifier, a demo device key and sensor values.

### Mosquitto broker

Mosquitto is the MQTT broker. In this first version, anonymous access is enabled to keep the project easy to run locally. The backend still validates device keys before storing telemetry.

### FastAPI backend

The backend subscribes to MQTT telemetry topics, validates payloads, checks the device registry and persists measurements in PostgreSQL. It also exposes REST endpoints for dashboards and external integrations.

### PostgreSQL

PostgreSQL stores registered devices, measurements and alerts. The schema is intentionally simple so the project remains readable.

### Vue dashboard

The dashboard consumes the REST API and displays live operational information: devices, latest measurements, alerts and platform statistics.

### Prometheus and Grafana

Prometheus collects backend metrics from `/metrics`. Grafana uses Prometheus as a datasource and displays a pre-provisioned dashboard.

## Data flow

```txt
Device simulator -> MQTT broker -> FastAPI consumer -> PostgreSQL -> REST API -> Vue dashboard
FastAPI backend -> Prometheus -> Grafana
```

## Why this architecture

The project separates ingestion, storage, visualization and monitoring. This makes the platform easier to debug and closer to how real IoT systems are organized.

## Extension points

- Replace the simulator with real ESP32 or Raspberry Pi devices.
- Add TLS and authentication to Mosquitto.
- Add Grafana dashboards for historical time-series visualization.
- Deploy the stack on Kubernetes.
- Replace rule-based anomaly detection with an AI model.
