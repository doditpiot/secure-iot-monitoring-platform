"""
Device API schemas.

Author: HAMAILI Ahmed-Imad
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DeviceCreate(BaseModel):
    """Payload required to register a new device."""

    device_id: str = Field(min_length=3, max_length=120)
    name: str = Field(min_length=2, max_length=160)
    location: str | None = Field(default=None, max_length=160)
    api_key: str = Field(min_length=8, max_length=160)
    protocol: str = Field(default="mqtt", max_length=40)


class DeviceOut(BaseModel):
    """Public representation of a registered device."""

    id: int
    device_id: str
    name: str
    location: str | None
    protocol: str
    status: str
    is_active: bool
    created_at: datetime
    last_seen_at: datetime | None

    # Allows Pydantic to serialize SQLAlchemy model instances directly.
    model_config = ConfigDict(from_attributes=True)


class DeviceCreatedOut(DeviceOut):
    """Response returned after creating a device.

    The raw key is not returned. Only a masked hint is shown.
    """

    api_key_hint: str
