from typing import Type, Callable, Any, Dict, List

from chamber.message import Message
from chamber.message.bus import MessageBus, M


class SynchronousMessageBus(MessageBus):
    def __init__(self):
        self._subscriptions: Dict[Type[M], List[Callable[[M], Any]]] = {}

    def subscribe(self, message: Type[M], handler: Callable[[M], Any]):
        self._subscriptions[message] = self._subscriptions.get(message, []) + [handler]

    def publish(self, message: Message):
        for handler in self._subscriptions.get(message.__class__, []):
            handler(message)
