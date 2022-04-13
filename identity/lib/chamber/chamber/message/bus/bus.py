from abc import ABC, abstractmethod
from typing import Callable, TypeVar, Any

from chamber.message import Message


M = TypeVar('M', bound=Message)


class MessageBus(ABC):
    @abstractmethod
    def publish(self, topic: str, message: Message):
        """
        :param topic:
        :param message:
        :raises:
            MessageTypeNotAllowedException
        """

    @abstractmethod
    def subscribe(self, topic: str, handler: Callable[[M], Any]):
        pass

    @abstractmethod
    def allow_publish_message(self, topic: str):
        pass
