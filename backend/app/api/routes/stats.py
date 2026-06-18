"""
Dashboard statistics routes.

Author: HAMAILI Ahmed-Imad
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.alert import Alert
from app.models.device import Device
from app.models.measurement import Measurement
from app.schemas.stats import PlatformSummary

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get("/summary", response_model=PlatformSummary)
def get_platform_summary(db: Session = Depends(get_db)):
    """Aggregate counters used by the Vue summary cards."""

    devices = db.query(Device).count()
    online_devices = db.query(Device).filter(Device.status == "online").count()
    measurements = db.query(Measurement).count()
    alerts = db.query(Alert).count()

    return PlatformSummary(
        devices=devices,
        online_devices=online_devices,
        measurements=measurements,
        alerts=alerts,
    )
