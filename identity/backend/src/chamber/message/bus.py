from abc import ABC, abstractmethod
from typing import Type, Callable, TypeVar, Any

from chamber.message.message import Message


M = TypeVar('M', bound=Message)


class MessageBus(ABC):
    @abstractmethod
    def publish(self, message: Message):
        pass

    @abstractmethod
    def subscribe(self, message: Type[M], handler: Callable[[M], Any]):
        pass
