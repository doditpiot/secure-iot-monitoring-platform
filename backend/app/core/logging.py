"""
Logging helpers.

Author: HAMAILI Ahmed-Imad
"""

import logging


def configure_logging() -> None:
    """Configure a small but readable logging format for local development."""

    # This format is short enough for Docker logs but still includes the module
    # name, which helps when debugging the MQTT consumer or database startup.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
