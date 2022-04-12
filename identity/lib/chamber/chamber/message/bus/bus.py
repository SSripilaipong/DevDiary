from abc import ABC, abstractmethod
from typing import Type, Callable, TypeVar, Any

from chamber.message import Message


M = TypeVar('M', bound=Message)


class MessageBus(ABC):
    @abstractmethod
    def publish(self, topic: str, message: Message, key: str = None):
        """
        :param topic:
        :param message:
        :param key:
        :raises:
            MessageTypeNotAllowedException
        """

    @abstractmethod
    def subscribe(self, message: Type[M], handler: Callable[[M], Any]):
        pass

    @abstractmethod
    def allow_publish_message(self, message: Type[Message]):
        pass
