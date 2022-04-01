from typing import Dict, Any, TypeVar, Callable

from lambler.base.handler import PatternMatcher, Handler
from lambler.base.response import LamblerResponse

T = TypeVar("T", bound=Callable)


class DynamodbEventHandler(Handler):
    def handle(self) -> LamblerResponse:
        pass


class DynamodbEventRouter(PatternMatcher):
    def __init__(self, stream_view_type):
        pass

    def match(self, event: Dict, context: Any) -> DynamodbEventHandler:
        pass

    def insert(self):
        def decorator(func: T) -> T:
            pass
        return decorator
