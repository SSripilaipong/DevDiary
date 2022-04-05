from typing import Callable, Any, Optional

from lambler.base.handler import PatternMatcher
from lambler.dynamodb_event.event import DynamodbEvent
from lambler.dynamodb_event.endpoint.handler import DynamodbEventHandler
from lambler.dynamodb_event.type import DynamodbEventType


class DynamodbEventEndpoint(PatternMatcher):
    def __init__(self, method: DynamodbEventType, handle: Callable):
        self._method = method
        self._handle = handle

    def match(self, event: DynamodbEvent, context: Any) -> Optional[DynamodbEventHandler]:
        return DynamodbEventHandler.create(self._method, self._handle, event)
