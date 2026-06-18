"""
Dashboard summary schemas.

Author: HAMAILI Ahmed-Imad
"""

from pydantic import BaseModel


class PlatformSummary(BaseModel):
    """Small set of counters displayed by the dashboard summary cards."""

    devices: int
    online_devices: int
    measurements: int
    alerts: int
