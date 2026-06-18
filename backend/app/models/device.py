"""
Device database model.

Author: HAMAILI Ahmed-Imad
"""

from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.db.session import Base


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp for database defaults."""

    return datetime.now(timezone.utc)


class Device(Base):
    """Registered IoT device allowed to publish telemetry."""

    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)

    # `device_id` is the public identifier used in MQTT topics and API results.
    device_id = Column(String(120), unique=True, index=True, nullable=False)
    name = Column(String(160), nullable=False)
    location = Column(String(160), nullable=True)
    protocol = Column(String(40), default="mqtt", nullable=False)

    # The raw key is never stored. Only its hash is kept in PostgreSQL.
    api_key_hash = Column(String(128), nullable=False)

    status = Column(String(40), default="offline", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    last_seen_at = Column(DateTime(timezone=True), nullable=True)
