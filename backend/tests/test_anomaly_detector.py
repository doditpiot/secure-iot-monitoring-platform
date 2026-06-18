"""
Tests for rule-based anomaly detection.

Author: HAMAILI Ahmed-Imad
"""

from app.services.anomaly_detector import detect_anomalies


def test_detects_high_temperature():
    """High temperature telemetry should create a critical alert."""

    alerts = detect_anomalies({"temperature": 50})
    assert any(alert.alert_type == "temperature_high" for alert in alerts)


def test_detects_low_battery():
    """Low battery telemetry should create a warning alert."""

    alerts = detect_anomalies({"battery": 10})
    assert any(alert.alert_type == "battery_low" for alert in alerts)


def test_normal_payload_has_no_alerts():
    """Normal telemetry should stay clean and generate no alerts."""

    alerts = detect_anomalies(
        {
            "temperature": 22,
            "humidity": 50,
            "battery": 80,
            "rssi": -55,
        }
    )
    assert alerts == []
