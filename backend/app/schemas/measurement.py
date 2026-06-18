"""
Measurement API schemas.

Author: HAMAILI Ahmed-Imad
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MeasurementOut(BaseModel):
    """Telemetry row returned by the REST API."""

    id: int
    device_id: str
    temperature: float | None = None
    humidity: float | None = None
    battery: float | None = None
    rssi: int | None = None
    status: str | None = None
    timestamp: datetime
    server_received_at: datetime

    model_config = ConfigDict(from_attributes=True)
