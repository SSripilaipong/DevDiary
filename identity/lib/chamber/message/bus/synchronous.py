from typing import Type, Callable, Any, Dict, List, Set, TypeVar

from chamber.message import Message
from chamber.message.bus import MessageBus
from chamber.message.exception import MessageTypeNotAllowedException


M = TypeVar('M', bound=Message)


class SynchronousMessageBus(MessageBus):
    def __init__(self):
        self._subscriptions: Dict[Type[M], List[Callable[[M], Any]]] = {}
        self._message_whitelist: Set[Type[Message]] = set()

    def subscribe(self, message: Type[M], handler: Callable[[M], Any]):
        self._subscriptions[message] = self._subscriptions.get(message, []) + [handler]

    def publish(self, message: Message):
        if message.__class__ not in self._message_whitelist:
            raise MessageTypeNotAllowedException(message.__class__.__name__)

        for handler in self._subscriptions.get(message.__class__, []):
            handler(message)

    def allow_publish_message(self, message: Type[Message]):
        self._message_whitelist.add(message)
