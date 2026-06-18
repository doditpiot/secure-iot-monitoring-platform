"""
Telemetry measurement database model.

Author: HAMAILI Ahmed-Imad
"""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String

from app.db.session import Base


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp for server-side timestamps."""

    return datetime.now(timezone.utc)


class Measurement(Base):
    """One telemetry sample received from a device."""

    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)

    # Measurements are linked to the device registry through the public device id.
    device_id = Column(String(120), ForeignKey("devices.device_id"), index=True, nullable=False)

    # Sensor fields are nullable because real IoT devices often send partial
    # payloads depending on the hardware profile or battery mode.
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    battery = Column(Float, nullable=True)
    rssi = Column(Integer, nullable=True)
    status = Column(String(50), nullable=True)

    # `timestamp` comes from the device. `server_received_at` is assigned by the
    # backend so ingestion delay can be studied later.
    timestamp = Column(DateTime(timezone=True), nullable=False)
    server_received_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
