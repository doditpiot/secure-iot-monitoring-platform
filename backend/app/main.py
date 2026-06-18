"""
FastAPI application entrypoint.

Author: HAMAILI Ahmed-Imad

This module wires together the HTTP API, the database bootstrap and the MQTT
consumer. The goal is to keep the application startup explicit: when the API
starts, it prepares the database and then listens for telemetry messages.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.alerts import router as alerts_router
from app.api.routes.devices import router as devices_router
from app.api.routes.health import router as health_router
from app.api.routes.measurements import router as measurements_router
from app.api.routes.metrics import router as metrics_router
from app.api.routes.stats import router as stats_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.db.init_db import init_database
from app.services.mqtt_consumer import start_mqtt_consumer

# Logging is configured once at import time so every service module shares the
# same readable output format inside Docker logs.
configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start and stop infrastructure tasks around the FastAPI lifecycle.

    FastAPI calls this context manager once during startup and once during
    shutdown. It is the right place to initialize database tables and to start
    the MQTT background loop, because both tasks belong to the backend runtime.
    """

    # Create tables and seed demo devices before the MQTT consumer starts. This
    # prevents the first simulator messages from being rejected as unknown.
    init_database()

    # The MQTT client runs in its own network loop. The returned client is kept
    # so it can be stopped cleanly when the backend container shuts down.
    mqtt_client = start_mqtt_consumer()

    yield

    # Clean shutdown keeps the container logs tidy and avoids leaving an active
    # MQTT loop behind when Docker stops or restarts the service.
    if mqtt_client:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Secure IoT monitoring platform with MQTT, FastAPI, PostgreSQL, Vue and Docker.",
    lifespan=lifespan,
)

# CORS is intentionally narrow for the local dashboard. In production, this
# list should be replaced by the real frontend domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes are grouped by domain so the API documentation remains clean.
app.include_router(health_router)
app.include_router(devices_router)
app.include_router(measurements_router)
app.include_router(alerts_router)
app.include_router(stats_router)
app.include_router(metrics_router)
