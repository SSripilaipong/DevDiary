from typing import Dict, List, Any

from lambler.base.handler.exception import NoHandlerMatchedException
from lambler.base.handler import PatternMatcher, Handler


class HandlerRouter(PatternMatcher):
    def __init__(self, handlers: List[PatternMatcher]):
        self._matchers = handlers

    def match(self, event: Dict, context: Any) -> Handler:
        for matcher in self._matchers:
            handler = matcher.match(event, context)
            if handler is not None:
                return handler
        raise NoHandlerMatchedException()

    @classmethod
    def from_list(cls, handlers: List[PatternMatcher]) -> 'HandlerRouter':
        return cls(handlers)
