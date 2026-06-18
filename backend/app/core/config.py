"""
Application configuration.

Author: HAMAILI Ahmed-Imad

The backend is configured through environment variables so the same code can run
locally, in Docker Compose or later in Kubernetes.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables or `.env`."""

    # Public API metadata displayed in the FastAPI documentation.
    app_name: str = "Secure IoT Monitoring Platform"
    app_version: str = "0.1.0"

    # Docker Compose resolves the hostname `postgres` to the PostgreSQL service.
    database_url: str = "postgresql+psycopg2://iot_user:iot_password@postgres:5432/iot_monitoring"

    # MQTT broker configuration. The wildcard topic receives telemetry from all
    # devices following the `iot/{device_id}/telemetry` topic convention.
    mqtt_host: str = "mqtt"
    mqtt_port: int = 1883
    mqtt_telemetry_topic: str = "iot/+/telemetry"

    # Frontend origins allowed to call the API in local development.
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
