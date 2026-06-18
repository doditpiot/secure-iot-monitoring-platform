"""
Alert database model.

Author: HAMAILI Ahmed-Imad
"""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.db.session import Base


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp for new alerts."""

    return datetime.now(timezone.utc)


class Alert(Base):
    """Anomaly or operational event generated from telemetry."""

    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(120), ForeignKey("devices.device_id"), index=True, nullable=False)
    severity = Column(String(40), nullable=False)
    alert_type = Column(String(80), nullable=False)
    message = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
