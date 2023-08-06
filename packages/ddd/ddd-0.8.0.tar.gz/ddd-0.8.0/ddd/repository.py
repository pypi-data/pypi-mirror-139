"""Declares :class:`Repository`."""
import abc
import logging

from .aggregateroot import AggregateRoot
from .const import DEFAULT_LOGGER_NAME
from .factory import Factory


class Repository(metaclass=abc.ABCMeta):
    """Provide a base class implementation for DDD repositories."""
    __module__: str = 'ddd'
    logger: logging.Logger = logging.getLogger(DEFAULT_LOGGER_NAME)

    @abc.abstractproperty
    def factory(self) -> Factory:
        """The :class:`ddd.Factory` implementation that is used to reconstruct
        :class:`ddd.AggregateRoot` instance from the persistence backend.
        """
        raise NotImplementedError

    async def exists(self, *args, **kwargs) -> bool:
        """Return a boolean indicating if the :class:`ddd.AggregateRoot`
        specified by the input parameters exists.
        """
        raise NotImplementedError

    async def persist(self, obj: AggregateRoot) -> AggregateRoot:
        """Persist an :class:`~ddd.AggregateRoot` instance and return the
        instance, reflecting any data changes that were made during the
        persist.
        """
        raise NotImplementedError

    async def __aenter__(self):
        if hasattr(self, 'setup_context'):
            await self.setup_context()
        return self

    async def __aexit__(self, type, exception, traceback) -> bool:
        suppress = False
        if hasattr(self, 'teardown_context'):
            suppress = await self.teardown_context(type, exception, traceback)
        return bool(suppress)
