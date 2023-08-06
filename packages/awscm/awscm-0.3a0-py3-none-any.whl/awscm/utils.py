"""Module contains generally used supporting functions."""

import logging
import os


def logger() -> logging:
    """Returns a logger object."""
    logger = logging.getLogger(__name__)
    logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))
    return logger
