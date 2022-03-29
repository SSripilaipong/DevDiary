from typing import Dict, List, Any

from lambler.base.handler.exception import NoHandlerMatchedException
from lambler.base.handler import HandlerMatcher, Handler


class HandlerRouter(HandlerMatcher):
    def __init__(self, handlers: List[HandlerMatcher]):
        self._matchers = handlers

    def match(self, event: Dict, context: Any) -> Handler:
        for matcher in self._matchers:
            handler = matcher.match(event, context)
            if handler is not None:
                return handler
        raise NoHandlerMatchedException()

    @classmethod
    def from_list(cls, handlers: List[HandlerMatcher]) -> 'HandlerRouter':
        return cls(handlers)
