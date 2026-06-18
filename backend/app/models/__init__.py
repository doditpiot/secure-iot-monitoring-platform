"""
SQLAlchemy model exports.

Author: HAMAILI Ahmed-Imad

Importing models here makes it easier for the database initialization module to
register every table before calling `Base.metadata.create_all`.
"""

from app.models.alert import Alert
from app.models.device import Device
from app.models.measurement import Measurement

__all__ = ["Alert", "Device", "Measurement"]
