"""Declares :class:`AggregateRoot`."""
import logging

from .const import DEFAULT_LOGGER_NAME


class AggregateRoot:
    """Encapsulates a domain model and represents an atomic unit through which
    data changes are made.
    """
    __module__: str = 'ddd'
    logger: logging.Logger = logging.getLogger(DEFAULT_LOGGER_NAME)
