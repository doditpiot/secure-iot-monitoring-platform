"""
Device registry API routes.

Author: HAMAILI Ahmed-Imad
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_api_key, mask_api_key
from app.db.session import get_db
from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceCreatedOut, DeviceOut

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.get("", response_model=list[DeviceOut])
def list_devices(db: Session = Depends(get_db)):
    """Return all registered devices ordered by their public identifier."""

    return db.query(Device).order_by(Device.device_id.asc()).all()


@router.post("", response_model=DeviceCreatedOut, status_code=status.HTTP_201_CREATED)
def create_device(payload: DeviceCreate, db: Session = Depends(get_db)):
    """Register a new MQTT device.

    The API receives a raw key only once. The database stores the hash, and the
    response returns a masked hint to confirm which key was used.
    """

    existing = db.query(Device).filter(Device.device_id == payload.device_id).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A device with this id already exists.",
        )

    device = Device(
        device_id=payload.device_id,
        name=payload.name,
        location=payload.location,
        protocol=payload.protocol,
        api_key_hash=hash_api_key(payload.api_key),
        status="offline",
        is_active=True,
    )

    db.add(device)
    db.commit()
    db.refresh(device)

    return DeviceCreatedOut.model_validate(device).model_copy(
        update={"api_key_hint": mask_api_key(payload.api_key)}
    )


@router.get("/{device_id}", response_model=DeviceOut)
def get_device(device_id: str, db: Session = Depends(get_db)):
    """Return one registered device by its public identifier."""

    device = db.query(Device).filter(Device.device_id == device_id).first()

    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found.")

    return device
