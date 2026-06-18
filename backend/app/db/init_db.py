"""
Database initialization and demo data seeding.

Author: HAMAILI Ahmed-Imad
"""

import logging
import time

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.security import hash_api_key
from app.db.session import Base, SessionLocal, engine
from app.models import Alert, Device, Measurement

logger = logging.getLogger(__name__)

# Demo devices are seeded so the simulator can publish valid telemetry
# immediately. In a real deployment, devices would be registered by an admin API
# or a provisioning workflow.
DEFAULT_DEVICES = [
    {
        "device_id": "esp32-room-01",
        "name": "Office climate sensor",
        "location": "Office room",
        "api_key": "room-01-demo-key",
    },
    {
        "device_id": "esp32-room-02",
        "name": "Meeting room climate sensor",
        "location": "Meeting room",
        "api_key": "room-02-demo-key",
    },
    {
        "device_id": "raspberry-lab-01",
        "name": "Lab edge gateway",
        "location": "IoT lab",
        "api_key": "raspberry-lab-demo-key",
    },
    {
        "device_id": "industrial-sensor-01",
        "name": "Industrial line sensor",
        "location": "Production line",
        "api_key": "industrial-sensor-demo-key",
    },
]


def wait_for_database(max_retries: int = 30, delay_seconds: int = 2) -> None:
    """Wait until PostgreSQL accepts connections.

    Docker Compose starts containers in order, but PostgreSQL may still need a
    few seconds before it is ready to accept SQL connections.
    """

    for attempt in range(1, max_retries + 1):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return
        except Exception as error:
            logger.info("Database not ready yet (%s/%s): %s", attempt, max_retries, error)
            time.sleep(delay_seconds)

    raise RuntimeError("Database is not available")


def seed_default_devices(db: Session) -> None:
    """Create demo devices when they do not already exist."""

    for item in DEFAULT_DEVICES:
        existing = db.query(Device).filter(Device.device_id == item["device_id"]).first()
        if existing:
            continue

        db.add(
            Device(
                device_id=item["device_id"],
                name=item["name"],
                location=item["location"],
                protocol="mqtt",
                api_key_hash=hash_api_key(item["api_key"]),
                status="offline",
                is_active=True,
            )
        )

    db.commit()


def init_database() -> None:
    """Create database tables and seed the demo registry."""

    wait_for_database()

    # Importing the models above registers them on the SQLAlchemy metadata. The
    # following call creates the tables if they are missing.
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        seed_default_devices(db)
    finally:
        db.close()
