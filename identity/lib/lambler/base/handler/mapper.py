from typing import Dict, List

from lambler.base.handler.exception import NoHandlerMatchedException
from lambler.base.handler.handler import HandlerMatcher


class ServiceEventHandlerMapper:
    def __init__(self, handlers: List[HandlerMatcher]):
        self._handlers = handlers

    def map(self, raw_event: Dict) -> HandlerMatcher:
        for handler in self._handlers:
            if handler.match(raw_event):
                return handler
        raise NoHandlerMatchedException()

    @classmethod
    def from_list(cls, handlers: List[HandlerMatcher]) -> 'ServiceEventHandlerMapper':
        return cls(handlers)
