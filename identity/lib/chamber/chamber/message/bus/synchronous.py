from typing import Callable, Any, Dict, List, Set, TypeVar

from chamber.message import Message
from chamber.message.bus import MessageBus
from chamber.message.exception import TopicNotAllowedException


M = TypeVar('M', bound=Message)


class SynchronousMessageBus(MessageBus):
    def __init__(self):
        self._subscriptions: Dict[str, List[Callable[[M], Any]]] = {}
        self._topic_whitelist: Set[str] = set()

    def subscribe(self, topic: str, handler: Callable[[M], Any]):
        self._subscriptions[topic] = self._subscriptions.get(topic, []) + [handler]

    def publish(self, topic: str, message: Message, key: str = None):
        if topic not in self._topic_whitelist:
            raise TopicNotAllowedException(topic)

        for handler in self._subscriptions.get(topic, []):
            handler(message)

    def allow_publish_message(self, topic: str):
        self._topic_whitelist.add(topic)
