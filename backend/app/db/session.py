"""
Database session setup.

Author: HAMAILI Ahmed-Imad
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

# `pool_pre_ping=True` helps recover from stale database connections after a
# container restart or short network interruption.
engine = create_engine(settings.database_url, pool_pre_ping=True)

# The session factory is used by both HTTP routes and the MQTT consumer.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# All SQLAlchemy models inherit from this base class.
Base = declarative_base()


def get_db():
    """Provide a database session for FastAPI routes.

    FastAPI dependencies can yield resources. The `finally` block guarantees that
    every request closes its session properly.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
