# Technical Documentation

**Author: HAMAILI Ahmed-Imad**

This document explains the main code paths of the Secure IoT Monitoring Platform. It is written as project documentation for anyone reviewing the repository or extending the platform.

## 1. Runtime flow

The platform starts through Docker Compose. The backend waits for PostgreSQL, creates the database tables, seeds demo devices and then starts the MQTT consumer.

```txt
docker compose up
  -> PostgreSQL starts
  -> Mosquitto starts
  -> FastAPI starts
  -> FastAPI initializes tables and demo devices
  -> FastAPI subscribes to MQTT telemetry
  -> IoT simulator publishes device messages
  -> Backend validates and stores measurements
  -> Frontend reads data through REST endpoints
  -> Prometheus scrapes /metrics
  -> Grafana displays Prometheus metrics
```

## 2. Backend modules

### `app/main.py`

Creates the FastAPI application, configures CORS, starts the database initialization and starts the MQTT consumer during the application lifespan.

### `app/core/config.py`

Centralizes runtime configuration. Values can come from default settings, Docker environment variables or a local `.env` file.

### `app/core/security.py`

Handles device API key hashing, key verification and safe key masking. The backend never stores demo keys in plain text inside PostgreSQL.

### `app/db/session.py`

Creates the SQLAlchemy engine, session factory and FastAPI dependency used by HTTP routes.

### `app/db/init_db.py`

Waits for PostgreSQL, creates tables and seeds demo devices so the simulator can send valid telemetry immediately after startup.

### `app/services/mqtt_consumer.py`

Subscribes to MQTT topics, decodes JSON payloads, validates the device identity, stores measurements and creates alerts when anomaly rules are triggered.

### `app/services/anomaly_detector.py`

Contains simple rule-based checks for high temperature, low temperature, high humidity, low battery and weak wireless signal.

### `app/services/metrics.py`

Defines Prometheus counters for MQTT messages, stored measurements, rejected messages and generated alerts.

## 3. Frontend modules

### `src/App.vue`

Loads platform data from the backend and refreshes the dashboard every few seconds.

### `src/services/api.ts`

Centralizes all REST calls used by the dashboard.

### `src/components/*`

Splits the dashboard into readable components: summary cards, device table, measurement table and alert list.

## 4. IoT simulator

The simulator reads `devices.json`, generates realistic random telemetry and publishes one MQTT message per device at a fixed interval. It occasionally injects abnormal values so the alert system can be demonstrated.

## 5. Observability

Prometheus scrapes the backend on `/metrics`. Grafana is automatically provisioned with a Prometheus datasource and a default dashboard.

## 6. Extension points

Possible improvements:

- Add user authentication for the dashboard.
- Add Mosquitto users and ACL rules.
- Replace rule-based anomaly detection with a small time-series model.
- Add MQTT over TLS.
- Add Kubernetes manifests.
- Add real ESP32 or Raspberry Pi devices.
- Add Grafana panels for business metrics such as online devices and message ingestion rate.


## IoT telemetry metrics exposed to Prometheus

The backend exports both system metrics and domain-specific IoT metrics. The domain metrics are updated when an MQTT message is accepted by the backend. This makes Grafana useful for more than infrastructure health: it can also display live sensor values.

| Metric | Type | Meaning |
| --- | --- | --- |
| `secure_iot_mqtt_messages_total` | Counter | Total MQTT messages received by the backend consumer. |
| `secure_iot_stored_measurements_total` | Counter | Total telemetry measurements stored in PostgreSQL. |
| `secure_iot_rejected_messages_total` | Counter | Messages rejected because of invalid JSON, unknown device or invalid device key. |
| `secure_iot_generated_alerts_total` | Counter | Alerts created by the rule-based anomaly detector. |
| `secure_iot_device_temperature_celsius` | Gauge | Latest temperature per device. |
| `secure_iot_device_humidity_percent` | Gauge | Latest humidity per device. |
| `secure_iot_device_battery_percent` | Gauge | Latest battery level per device. |
| `secure_iot_device_rssi_dbm` | Gauge | Latest wireless signal strength per device. |
| `secure_iot_device_online` | Gauge | Per-device online flag. |
| `secure_iot_active_devices_total` | Gauge | Number of registered devices currently marked online. |

Grafana uses these metrics to show live temperature, humidity, battery level, RSSI, message rates, rejected messages and backend resource usage.
