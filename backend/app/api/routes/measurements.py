"""
Measurement API routes.

Author: HAMAILI Ahmed-Imad
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.measurement import Measurement
from app.schemas.measurement import MeasurementOut

router = APIRouter(prefix="/measurements", tags=["Measurements"])


@router.get("/latest", response_model=list[MeasurementOut])
def get_latest_measurements(
    limit: int = Query(default=50, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """Return the most recent telemetry rows across every device."""

    return (
        db.query(Measurement)
        .order_by(Measurement.timestamp.desc())
        .limit(limit)
        .all()
    )


@router.get("/devices/{device_id}", response_model=list[MeasurementOut])
def get_device_measurements(
    device_id: str,
    limit: int = Query(default=100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """Return recent telemetry for one selected device."""

    return (
        db.query(Measurement)
        .filter(Measurement.device_id == device_id)
        .order_by(Measurement.timestamp.desc())
        .limit(limit)
        .all()
    )
