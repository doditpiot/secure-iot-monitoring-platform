"""
Prometheus metrics route.

Author: HAMAILI Ahmed-Imad
"""

from fastapi import APIRouter, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

router = APIRouter(tags=["Metrics"])


@router.get("/metrics")
def get_metrics():
    """Expose backend metrics in Prometheus text format."""

    # Prometheus scrapes this endpoint from inside the Docker network using the
    # service name `backend:8000`.
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
