from typing import Callable, Any, Optional

from lambler.base.function import MarkedFunction
from lambler.base.handler import PatternMatcher
from lambler.dynamodb_event.data.event import DynamodbEvent
from lambler.dynamodb_event.endpoint.handler import DynamodbEventHandler
from lambler.dynamodb_event.data.type import DynamodbEventType
from lambler.dynamodb_event.input.collection import DynamodbEventInputCollection


class DynamodbEventEndpoint(PatternMatcher):
    def __init__(self, method: DynamodbEventType, handle: MarkedFunction):
        self._method = method
        self._handle = handle

    @classmethod
    def create(cls, method: DynamodbEventType, handle: Callable) -> 'DynamodbEventEndpoint':
        return cls(method, MarkedFunction.from_function(handle))

    def match(self, event: DynamodbEvent, context: Any) -> Optional[DynamodbEventHandler]:
        return DynamodbEventHandler.create(self._method, self._handle, DynamodbEventInputCollection.from_event(event))
