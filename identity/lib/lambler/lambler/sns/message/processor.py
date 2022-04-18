from typing import Optional, TypeVar, Callable, Dict, Iterator, List

from lambler.base.event import LamblerEvent
from lambler.base.handler import PatternMatcher, Handler
from lambler.base.router import Router
from lambler.sns.message.endpoint import SNSMessageEndpoint

T = TypeVar("T", bound=Callable)


class SNSMessageProcessor(Router):
    def __init__(self):
        self._endpoints: List[PatternMatcher] = []

    def _iterate_patterns(self) -> Iterator[PatternMatcher]:
        return self._endpoints

    def _validate_event(self, event: Dict) -> Optional[LamblerEvent]:
        return LamblerEvent()

    def _on_no_pattern_matched(self, event: LamblerEvent) -> Optional[Handler]:
        pass  # TODO: implement

    def message(self, topic_name: str):
        def decorator(func: T) -> T:
            self._endpoints.append(SNSMessageEndpoint(func))
            return func
        return decorator
