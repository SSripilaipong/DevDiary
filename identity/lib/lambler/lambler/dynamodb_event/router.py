from typing import Dict, Any, TypeVar, Callable, List

from lambler.base.handler import PatternMatcher, Handler
from lambler.base.response import LamblerResponse
from lambler.dynamodb_event.endpoint import DynamodbEventEndpoint
from lambler.dynamodb_event.event import DynamodbEvent
from lambler.dynamodb_event.type import DynamodbEventType

T = TypeVar("T", bound=Callable)


class DynamodbEventHandler(Handler):
    def __init__(self, endpoint: DynamodbEventEndpoint, event: DynamodbEvent):
        pass

    def handle(self) -> LamblerResponse:
        pass


class DynamodbEventRouter(PatternMatcher):
    def __init__(self, stream_view_type):
        self._endpoints: List[DynamodbEventEndpoint] = []

    def match(self, event: Dict, context: Any) -> DynamodbEventHandler:
        event: DynamodbEvent = self._validate_event(event)
        for endpoint in self._endpoints:
            if endpoint.accept(event):
                return DynamodbEventHandler(endpoint, event)

    def insert(self):
        def decorator(func: T) -> T:
            self._append_endpoint(DynamodbEventEndpoint(method=DynamodbEventType.INSERT, handle=func))
            return func
        return decorator

    def _append_endpoint(self, endpoint):
        self._endpoints.append(endpoint)

    def _validate_event(self, event) -> DynamodbEvent:
        try:
            return DynamodbEvent(**event)
        except:
            pass  # TODO: implement this
