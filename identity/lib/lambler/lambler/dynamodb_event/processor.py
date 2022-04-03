from typing import Dict, Any, TypeVar, Callable, List, Optional

from lambler.base.handler import PatternMatcher, Handler
from lambler.dynamodb_event.response import DynamodbEventBatchResponse
from lambler.dynamodb_event.router import DynamodbEventHandler, DynamodbEventRouter


T = TypeVar("T", bound=Callable)


class DynamodbEventBatchHandler(Handler):
    def __init__(self, handlers: List[DynamodbEventHandler]):
        self._handlers = handlers

    def handle(self) -> DynamodbEventBatchResponse:
        for handler in self._handlers:
            try:
                handler.handle()
            except:
                raise NotImplementedError()
        return DynamodbEventBatchResponse()


class DynamodbEventProcessor(PatternMatcher):
    def __init__(self, stream_view_type):
        self._router = DynamodbEventRouter()

    def match(self, event: Dict, context: Any) -> Optional[DynamodbEventBatchHandler]:
        records = event.get("Records", None)
        if records is None:
            return None

        return self.__make_batch_handler(records, context)

    def __make_batch_handler(self, records: List[Dict], context: Any) -> Optional[DynamodbEventBatchHandler]:
        handlers = []
        for record in records:
            matched_handler = self._router.match(record, context)
            if matched_handler is None:
                return None
            handlers.append(matched_handler)
        return DynamodbEventBatchHandler(handlers)

    def insert(self):
        def decorator(func: T) -> T:
            self._router.subscribe_insert(handle=func)
            return func
        return decorator
