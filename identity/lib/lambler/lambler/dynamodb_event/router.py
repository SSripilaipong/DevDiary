import pydantic
from typing import Callable, List, Optional, Iterator, TYPE_CHECKING, Any, Dict

from lambler.base.event import LamblerEvent
from lambler.base.handler import Handler, PatternMatcher
from lambler.base.router import Router
from lambler.dynamodb_event.endpoint import DynamodbEventEndpoint, DynamodbEventHandler
from lambler.dynamodb_event.event import DynamodbEvent
from lambler.dynamodb_event.type import DynamodbEventType


class DynamodbEventRouter(Router):
    def __init__(self):
        self._endpoints: List[DynamodbEventEndpoint] = []

    def subscribe_insert(self, handle: Callable):
        self._endpoints.append(DynamodbEventEndpoint(method=DynamodbEventType.INSERT, handle=handle))

    def _validate_event(self, event) -> Optional[DynamodbEvent]:
        try:
            return DynamodbEvent(**event)
        except pydantic.ValidationError:
            return None

    def _iterate_patterns(self) -> Iterator[PatternMatcher]:
        yield from self._endpoints

    def _on_no_pattern_matched(self, event: LamblerEvent) -> Optional[Handler]:
        pass

    if TYPE_CHECKING:
        def match(self, event: Dict, context: Any) -> Optional[DynamodbEventHandler]: ...
