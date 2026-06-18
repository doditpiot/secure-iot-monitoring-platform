"""
Alert API schemas.

Author: HAMAILI Ahmed-Imad
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AlertOut(BaseModel):
    """Alert row returned by the REST API."""

    id: int
    device_id: str
    severity: str
    alert_type: str
    message: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
