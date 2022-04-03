from typing import Callable

from lambler.base.router.endpoint import Endpoint
from lambler.dynamodb_event.event import DynamodbEvent
from lambler.dynamodb_event.type import DynamodbEventType


class DynamodbEventEndpoint(Endpoint):
    def __init__(self, method: DynamodbEventType, handle: Callable):
        self._method = method
        self._handle = handle

    def can_accept(self, event: DynamodbEvent) -> bool:
        return True
