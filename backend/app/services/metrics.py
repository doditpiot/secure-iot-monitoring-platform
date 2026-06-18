"""
Custom Prometheus metrics.

Author: HAMAILI Ahmed-Imad

The metrics in this module are intentionally separated from the MQTT consumer.
It keeps the ingestion logic readable while making the observability layer easy
to extend. Prometheus scrapes these values from `/metrics`, then Grafana uses
those time series to build the operational dashboard.
"""

from prometheus_client import Counter, Gauge

# These counters follow the main telemetry pipeline. They answer questions such
# as: "How many MQTT messages arrived?", "How many rows were stored?" and
# "How many messages were rejected before reaching the database?".
mqtt_messages_total = Counter(
    "secure_iot_mqtt_messages_total",
    "Total number of MQTT messages received by the backend.",
)

stored_measurements_total = Counter(
    "secure_iot_stored_measurements_total",
    "Total number of telemetry measurements stored in the database.",
)

rejected_messages_total = Counter(
    "secure_iot_rejected_messages_total",
    "Total number of MQTT messages rejected by validation.",
)

generated_alerts_total = Counter(
    "secure_iot_generated_alerts_total",
    "Total number of alerts generated from telemetry rules.",
)

# These gauges expose the latest known telemetry values per device. Grafana can
# display them as real-time charts, one line per sensor/device.
device_temperature_celsius = Gauge(
    "secure_iot_device_temperature_celsius",
    "Latest temperature reported by each device in Celsius.",
    ["device_id"],
)

device_humidity_percent = Gauge(
    "secure_iot_device_humidity_percent",
    "Latest humidity reported by each device in percent.",
    ["device_id"],
)

device_battery_percent = Gauge(
    "secure_iot_device_battery_percent",
    "Latest battery level reported by each device in percent.",
    ["device_id"],
)

device_rssi_dbm = Gauge(
    "secure_iot_device_rssi_dbm",
    "Latest wireless signal strength reported by each device in dBm.",
    ["device_id"],
)

device_online = Gauge(
    "secure_iot_device_online",
    "Device online status based on accepted telemetry. 1 means online, 0 means offline.",
    ["device_id"],
)

device_last_seen_timestamp_seconds = Gauge(
    "secure_iot_device_last_seen_timestamp_seconds",
    "Unix timestamp of the latest accepted telemetry message per device.",
    ["device_id"],
)

# This gauge is not labeled because it represents a platform-level summary.
active_devices_total = Gauge(
    "secure_iot_active_devices_total",
    "Number of active devices currently marked as online.",
)


def set_optional_gauge(gauge: Gauge, device_id: str, value: object) -> None:
    """Update a device gauge only when the incoming value is numeric.

    MQTT payloads are external inputs, so the metric layer stays defensive. If a
    sensor field is missing or malformed, the old metric value remains visible
    instead of crashing the ingestion loop.
    """

    if isinstance(value, bool):
        return

    if isinstance(value, (int, float)):
        gauge.labels(device_id=device_id).set(float(value))
