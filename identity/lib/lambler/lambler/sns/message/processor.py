from typing import Optional, TypeVar, Callable, Dict, Iterator, List

from lambler.base.handler import PatternMatcher
from lambler.base.router import Router
from lambler.sns.message.endpoint import SNSMessageEndpoint
from lambler.sns.message.event import SNSMessageEvent
from lambler.sns.message.handler import SNSMessageHandler

T = TypeVar("T", bound=Callable)


class SNSMessageProcessor(Router):
    def __init__(self):
        self._endpoints: List[PatternMatcher] = []

    def _iterate_patterns(self) -> Iterator[PatternMatcher]:
        return self._endpoints

    def _validate_event(self, event: Dict) -> Optional[SNSMessageEvent]:
        return SNSMessageEvent(**event)

    def _on_no_pattern_matched(self, event: SNSMessageEvent) -> Optional[SNSMessageHandler]:
        pass  # TODO: implement

    def message(self, topic_name: str):
        def decorator(func: T) -> T:
            self._endpoints.append(SNSMessageEndpoint.create(topic_name, func))
            return func
        return decorator
