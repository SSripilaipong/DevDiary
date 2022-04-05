import pydantic
from typing import Callable, List, Optional, Iterator, TYPE_CHECKING, Any, Dict

from lambler.base.event import LamblerEvent
from lambler.base.handler import Handler
from lambler.base.router import Router
from lambler.base.router.endpoint import Endpoint
from lambler.dynamodb_event.endpoint import DynamodbEventEndpoint
from lambler.dynamodb_event.event import DynamodbEvent
from lambler.dynamodb_event.response import DynamodbEventResponse
from lambler.dynamodb_event.type import DynamodbEventType


class DynamodbEventHandler(Handler):
    def __init__(self, endpoint: DynamodbEventEndpoint, event: DynamodbEvent):
        self._endpoint = endpoint
        self._event = event

    def handle(self) -> DynamodbEventResponse:
        return self._endpoint.process(self._event)


class DynamodbEventRouter(Router):
    def __init__(self):
        self._endpoints: List[DynamodbEventEndpoint] = []

    def subscribe_insert(self, handle: Callable):
        self._append_endpoint(DynamodbEventEndpoint(method=DynamodbEventType.INSERT, handle=handle))

    def _append_endpoint(self, endpoint):
        self._endpoints.append(endpoint)

    def _validate_event(self, event) -> Optional[DynamodbEvent]:
        try:
            return DynamodbEvent(**event)
        except pydantic.ValidationError:
            return None

    def _iterate_endpoints(self) -> Iterator[Endpoint]:
        yield from self._endpoints

    def _make_handler(self, endpoint: DynamodbEventEndpoint, event: DynamodbEvent) -> Handler:
        return DynamodbEventHandler(endpoint, event)

    def _on_no_pattern_matched(self, event: LamblerEvent) -> Optional[Handler]:
        pass

    if TYPE_CHECKING:
        def match(self, event: Dict, context: Any) -> Optional[DynamodbEventHandler]: ...
