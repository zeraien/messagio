import logging
import typing
from abc import ABC, abstractmethod

from .const import Messagio, TASK_PRIORITY

logger = logging.getLogger("messagio")

ListenerFunction = typing.Callable[[type(Messagio)], typing.Union[None, typing.Any]]


class AbstractMessageCenter(ABC):
    _instance = None

    @classmethod
    def singleton(cls) -> "AbstractMessageCenter":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    @abstractmethod
    def send(cls, messagio: Messagio, sync: bool = False):
        """
        send a message to all who would listen.

        :param messagio: message type as a string or Enum
        :param sync: send message synchronously
        """

    @abstractmethod
    def unsubscribe(
        self,
        event_type: typing.Type[Messagio],
        func: ListenerFunction,
    ):
        """
        stop listening to messages of the provided type
        :param event_type:
        :param func:
        :return:
        """

    @abstractmethod
    def subscribe(
        self,
        event_type: typing.Type[Messagio],
        func: ListenerFunction,
        priority: int = TASK_PRIORITY.REGULAR,
        autoretry_for: tuple[Exception] = tuple(),
        max_retries: int = None,
        default_retry_delay: float = None,
    ):
        """
        Subscribed function will be called whenever an event of the subscribed type is fired.

        :param priority: priority of the task, relevant to queue managers
        :param autoretry_for: list of exceptions that allow this to auto-retry
        :param max_retries: max number of times to retry the function call
        :param default_retry_delay: how many seconds to wait before retrying
        """
