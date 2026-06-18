"""
Rule-based anomaly detection.

Author: HAMAILI Ahmed-Imad

This module is intentionally simple. It gives the platform a useful first layer
of intelligence before replacing it with AI/time-series models in a future step.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class AlertCandidate:
    """Temporary alert object returned before it is stored in the database."""

    severity: str
    alert_type: str
    message: str


def detect_anomalies(payload: dict) -> list[AlertCandidate]:
    """Apply simple rule-based checks to incoming telemetry.

    The function stays independent from SQLAlchemy so it can be tested easily and
    later replaced by a more advanced anomaly detection model.
    """

    alerts: list[AlertCandidate] = []

    temperature = payload.get("temperature")
    humidity = payload.get("humidity")
    battery = payload.get("battery")
    rssi = payload.get("rssi")

    # Temperature thresholds are intentionally broad because the simulator mixes
    # office sensors, gateways and industrial sensors.
    if temperature is not None and temperature > 45:
        alerts.append(
            AlertCandidate(
                severity="critical",
                alert_type="temperature_high",
                message=f"Temperature is unusually high: {temperature}°C",
            )
        )

    if temperature is not None and temperature < -5:
        alerts.append(
            AlertCandidate(
                severity="warning",
                alert_type="temperature_low",
                message=f"Temperature is unusually low: {temperature}°C",
            )
        )

    if humidity is not None and humidity > 90:
        alerts.append(
            AlertCandidate(
                severity="warning",
                alert_type="humidity_high",
                message=f"Humidity is above expected range: {humidity}%",
            )
        )

    if battery is not None and battery < 15:
        alerts.append(
            AlertCandidate(
                severity="warning",
                alert_type="battery_low",
                message=f"Battery level is low: {battery}%",
            )
        )

    if rssi is not None and rssi < -85:
        alerts.append(
            AlertCandidate(
                severity="warning",
                alert_type="weak_signal",
                message=f"Wireless signal is weak: {rssi} dBm",
            )
        )

    return alerts
