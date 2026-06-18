"""
MQTT telemetry consumer.

Author: HAMAILI Ahmed-Imad

The consumer is the ingestion point of the platform. It receives messages from
Mosquitto, validates the device identity, stores measurements and generates
alerts when telemetry looks abnormal.
"""

import json
import logging
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

from app.core.config import settings
from app.core.security import verify_api_key
from app.db.session import SessionLocal
from app.models.alert import Alert
from app.models.device import Device
from app.models.measurement import Measurement
from app.services.anomaly_detector import detect_anomalies
from app.services.metrics import (
    active_devices_total,
    device_battery_percent,
    device_humidity_percent,
    device_last_seen_timestamp_seconds,
    device_online,
    device_rssi_dbm,
    device_temperature_celsius,
    generated_alerts_total,
    mqtt_messages_total,
    rejected_messages_total,
    set_optional_gauge,
    stored_measurements_total,
)

logger = logging.getLogger(__name__)


def parse_timestamp(value: str | None) -> datetime:
    """Parse an ISO timestamp and fall back to the current UTC time."""

    if not value:
        return datetime.now(timezone.utc)

    try:
        # The simulator uses ISO timestamps. The replace keeps compatibility with
        # payloads ending in `Z`, which is a common UTC notation in APIs.
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return datetime.now(timezone.utc)


def get_required_string(payload: dict, key: str) -> str | None:
    """Extract a required non-empty string from the MQTT payload."""

    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        return None

    return value.strip()


def update_iot_prometheus_metrics(payload: dict, device_id: str, online_devices: int) -> None:
    """Publish the latest IoT telemetry values to Prometheus gauges.

    The database remains the source of truth for historical data. These gauges
    only expose the most recent values so Grafana can display live temperature,
    humidity, battery and RSSI charts without querying PostgreSQL directly.
    """

    set_optional_gauge(device_temperature_celsius, device_id, payload.get("temperature"))
    set_optional_gauge(device_humidity_percent, device_id, payload.get("humidity"))
    set_optional_gauge(device_battery_percent, device_id, payload.get("battery"))
    set_optional_gauge(device_rssi_dbm, device_id, payload.get("rssi"))

    # A successfully accepted payload means the device is alive from the
    # platform point of view. Offline detection can be added later with a
    # scheduled task that checks `last_seen_at` timestamps.
    device_online.labels(device_id=device_id).set(1)
    device_last_seen_timestamp_seconds.labels(device_id=device_id).set(time.time())
    active_devices_total.set(online_devices)


def process_telemetry_payload(payload: dict) -> None:
    """Validate, store and analyze one telemetry payload."""

    device_id = get_required_string(payload, "device_id")
    device_key = get_required_string(payload, "device_key")

    # A message without identity cannot be trusted or linked to a device.
    if not device_id or not device_key:
        rejected_messages_total.inc()
        logger.warning("Rejected telemetry without device_id or device_key")
        return

    db = SessionLocal()

    try:
        device = db.query(Device).filter(Device.device_id == device_id).first()

        # Unknown or disabled devices are ignored. This keeps the registry as the
        # source of truth for what is allowed to publish telemetry.
        if not device or not device.is_active:
            rejected_messages_total.inc()
            logger.warning("Rejected telemetry from unknown or inactive device: %s", device_id)
            return

        if not verify_api_key(device_key, device.api_key_hash):
            rejected_messages_total.inc()
            logger.warning("Rejected telemetry with invalid device key: %s", device_id)
            return

        measurement = Measurement(
            device_id=device_id,
            temperature=payload.get("temperature"),
            humidity=payload.get("humidity"),
            battery=payload.get("battery"),
            rssi=payload.get("rssi"),
            status=payload.get("status", "online"),
            timestamp=parse_timestamp(payload.get("timestamp")),
        )

        # Updating the device status gives the dashboard a simple online/offline
        # indicator based on the latest accepted telemetry.
        device.status = "online"
        device.last_seen_at = datetime.now(timezone.utc)

        db.add(measurement)

        # Alerts are generated before the commit so measurements and alerts are
        # persisted together.
        for candidate in detect_anomalies(payload):
            db.add(
                Alert(
                    device_id=device_id,
                    severity=candidate.severity,
                    alert_type=candidate.alert_type,
                    message=candidate.message,
                )
            )
            generated_alerts_total.inc()

        # SQLAlchemy automatically flushes pending changes before this query.
        # The result is used by Grafana to display how many registered devices
        # are currently considered online.
        online_devices = (
            db.query(Device)
            .filter(Device.status == "online", Device.is_active == True)  # noqa: E712
            .count()
        )

        db.commit()
        stored_measurements_total.inc()
        update_iot_prometheus_metrics(payload, device_id, online_devices)
        logger.info("Stored telemetry from %s", device_id)
    except Exception as error:
        db.rollback()
        logger.exception("Failed to process telemetry: %s", error)
    finally:
        db.close()


def on_connect(client, userdata, flags, rc):
    """Subscribe to telemetry topics when the MQTT connection is ready."""

    if rc == 0:
        logger.info("MQTT backend consumer connected")
        client.subscribe(settings.mqtt_telemetry_topic)
        logger.info("Subscribed to MQTT topic: %s", settings.mqtt_telemetry_topic)
    else:
        logger.error("MQTT connection failed with code: %s", rc)


def on_message(client, userdata, message):
    """Handle one MQTT message delivered by the broker."""

    mqtt_messages_total.inc()

    try:
        payload = json.loads(message.payload.decode("utf-8"))
        process_telemetry_payload(payload)
    except json.JSONDecodeError:
        rejected_messages_total.inc()
        logger.warning("Rejected invalid JSON message on topic %s", message.topic)
    except Exception as error:
        rejected_messages_total.inc()
        logger.exception("Unexpected MQTT processing error: %s", error)


def start_mqtt_consumer(max_retries: int = 30, delay_seconds: int = 2) -> mqtt.Client | None:
    """Connect to the MQTT broker and start the consumer loop."""

    client = mqtt.Client(client_id="secure-iot-backend-consumer")
    client.on_connect = on_connect
    client.on_message = on_message

    # The retry loop handles the common Docker case where the backend starts
    # before Mosquitto is fully ready.
    for attempt in range(1, max_retries + 1):
        try:
            logger.info(
                "Connecting MQTT consumer to %s:%s",
                settings.mqtt_host,
                settings.mqtt_port,
            )
            client.connect(settings.mqtt_host, settings.mqtt_port, keepalive=60)
            client.loop_start()
            return client
        except Exception as error:
            logger.info("MQTT broker not ready yet (%s/%s): %s", attempt, max_retries, error)
            time.sleep(delay_seconds)

    logger.error("MQTT consumer could not connect after retries")
    return None
