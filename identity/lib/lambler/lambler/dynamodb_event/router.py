from typing import TypeVar, Callable, List, Optional, Iterator

from lambler.base.event import LamblerEvent
from lambler.base.handler import Handler
from lambler.base.response import LamblerResponse
from lambler.base.router import Router
from lambler.base.router.endpoint import Endpoint
from lambler.dynamodb_event.endpoint import DynamodbEventEndpoint
from lambler.dynamodb_event.event import DynamodbEvent
from lambler.dynamodb_event.type import DynamodbEventType

T = TypeVar("T", bound=Callable)


class DynamodbEventHandler(Handler):
    def __init__(self, endpoint: DynamodbEventEndpoint, event: DynamodbEvent):
        pass

    def handle(self) -> LamblerResponse:
        pass


class DynamodbEventRouter(Router):
    def __init__(self, stream_view_type):
        self._endpoints: List[DynamodbEventEndpoint] = []

    def insert(self):
        def decorator(func: T) -> T:
            self._append_endpoint(DynamodbEventEndpoint(method=DynamodbEventType.INSERT, handle=func))
            return func
        return decorator

    def _append_endpoint(self, endpoint):
        self._endpoints.append(endpoint)

    def _validate_event(self, event) -> Optional[DynamodbEvent]:
        try:
            return DynamodbEvent(**event)
        except:
            return None

    def _iterate_endpoints(self) -> Iterator[Endpoint]:
        yield from self._endpoints

    def _make_handler(self, endpoint: DynamodbEventEndpoint, event: DynamodbEvent) -> Handler:
        return DynamodbEventHandler(endpoint, event)

    def _on_no_endpoint_matched(self, event: LamblerEvent) -> Optional[Handler]:
        pass
