from typing import Any, Optional, Callable

from lambler.base.handler import PatternMatcher, Handler
from lambler.sns.message.event import SNSMessageEvent
from lambler.sns.message.handler import SNSMessageHandler, SNSMessageIgnorer


class SNSMessageEndpoint(PatternMatcher):
    def __init__(self, topic_name: str, handle: Callable):
        self._topic_name = topic_name
        self._handle = handle

    def match(self, event: SNSMessageEvent, context: Any) -> Optional[Handler]:
        if len(event.records) != 1:
            return None
        record = event.records[0]

        if not record.sns.topic_arn.endswith(f":{self._topic_name}"):
            return SNSMessageIgnorer()

        return SNSMessageHandler(self._handle)
