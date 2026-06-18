"""
MQTT IoT device simulator.

Author: HAMAILI Ahmed-Imad

The simulator gives the platform realistic input without needing physical ESP32
or Raspberry Pi devices. It reads demo device definitions, generates telemetry
and publishes the messages to Mosquitto.
"""

import json
import os
import random
import time
from datetime import datetime, timezone
from pathlib import Path

import paho.mqtt.client as mqtt

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
PUBLISH_INTERVAL = int(os.getenv("MQTT_PUBLISH_INTERVAL", "2"))
DEVICES_FILE = Path(__file__).with_name("devices.json")


def load_devices() -> list[dict]:
    """Load demo devices from the JSON configuration file."""

    with DEVICES_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def maybe_create_anomaly(value: float, probability: float, anomalous_value: float) -> float:
    """Inject rare abnormal values so the alert system can be demonstrated."""

    if random.random() < probability:
        return anomalous_value

    return value


def generate_measurement(device: dict) -> dict:
    """Generate one telemetry payload for a simulated device."""

    profile = device.get("profile", "indoor")

    # Different profiles produce slightly different sensor ranges. This makes the
    # dashboard more interesting than using one random range for every device.
    if profile == "industrial":
        temperature = random.uniform(28.0, 42.0)
        humidity = random.uniform(30.0, 65.0)
    elif profile == "edge-gateway":
        temperature = random.uniform(24.0, 38.0)
        humidity = random.uniform(35.0, 70.0)
    else:
        temperature = random.uniform(18.0, 30.0)
        humidity = random.uniform(35.0, 75.0)

    # Rare anomalies create real alerts without making the dashboard noisy all
    # the time.
    temperature = maybe_create_anomaly(temperature, probability=0.03, anomalous_value=random.uniform(46.0, 55.0))
    battery = maybe_create_anomaly(random.uniform(20.0, 100.0), probability=0.04, anomalous_value=random.uniform(5.0, 12.0))
    rssi = int(maybe_create_anomaly(random.randint(-75, -40), probability=0.04, anomalous_value=random.randint(-95, -87)))

    return {
        "device_id": device["device_id"],
        "device_key": device["device_key"],
        "temperature": round(temperature, 2),
        "humidity": round(humidity, 2),
        "battery": round(battery, 2),
        "rssi": rssi,
        "status": "online",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def connect_with_retry(client: mqtt.Client, max_retries: int = 30, delay_seconds: int = 2) -> None:
    """Connect to the MQTT broker, retrying while Mosquitto starts."""

    for attempt in range(1, max_retries + 1):
        try:
            print(f"Connecting simulator to MQTT broker at {MQTT_HOST}:{MQTT_PORT}")
            client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
            return
        except Exception as error:
            print(f"MQTT broker not ready yet ({attempt}/{max_retries}): {error}")
            time.sleep(delay_seconds)

    raise RuntimeError("Simulator could not connect to MQTT broker")


def main() -> None:
    """Run the simulator loop and publish telemetry forever."""

    devices = load_devices()
    client = mqtt.Client(client_id="secure-iot-device-simulator")
    connect_with_retry(client)
    client.loop_start()

    while True:
        for device in devices:
            payload = generate_measurement(device)
            topic = f"iot/{device['device_id']}/telemetry"
            client.publish(topic, json.dumps(payload))
            print(f"Published telemetry to {topic}: {payload}")

        time.sleep(PUBLISH_INTERVAL)


if __name__ == "__main__":
    main()
