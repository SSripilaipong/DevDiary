import json

from typing import Callable, Any, Set

from chamber.message import Message
from chamber.message.bus import MessageBus
from chamber.message.bus.bus import M
from chamber.message.exception import TopicNotAllowedException


class SNSMessageBus(MessageBus):
    def __init__(self, client, account_id: str, region: str, prefix: str = ""):
        self._client = client
        self._account_id = account_id
        self._region = region

        self._arn_prefix = f"arn:aws:sns:{self._region}:{self._account_id}:{prefix}"
        self._allowed_topics: Set[str] = set()

    def publish(self, topic: str, message: Message):
        if topic not in self._allowed_topics:
            raise TopicNotAllowedException()

        content = message.to_dict()
        _ = self._client.publish(
            TopicArn=self._arn_prefix + topic,
            Message=json.dumps({'default': json.dumps(content)}),
            MessageStructure='json'
        )

    def subscribe(self, topic: str, handler: Callable[[M], Any]):
        pass  # TODO: implement

    def allow_publish_message(self, topic: str):
        self._allowed_topics.add(topic)
