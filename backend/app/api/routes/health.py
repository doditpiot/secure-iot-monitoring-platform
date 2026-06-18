"""
Health-check endpoint.

Author: HAMAILI Ahmed-Imad
"""

from fastapi import APIRouter
from sqlalchemy import text

from app.db.session import engine

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
def health_check():
    """Return service health and database availability."""

    database_status = "ok"

    try:
        # A lightweight SQL query is enough to verify that the database is alive.
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception:
        database_status = "unavailable"

    return {
        "status": "ok" if database_status == "ok" else "degraded",
        "service": "secure-iot-monitoring-platform",
        "database": database_status,
    }
