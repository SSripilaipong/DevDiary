from typing import Dict, Any, TypeVar, Callable, List, Optional

from lambler import logger
from lambler.base.handler import PatternMatcher, Handler
from lambler.dynamodb_event.response import DynamodbEventBatchResponse
from lambler.dynamodb_event.router import DynamodbEventRouter
from lambler.dynamodb_event.endpoint import DynamodbEventHandler

T = TypeVar("T", bound=Callable)


class DynamodbEventBatchHandler(Handler):
    def __init__(self, handlers: List[DynamodbEventHandler]):
        self._handlers = handlers

    def handle(self) -> DynamodbEventBatchResponse:
        self.__log_on_start()
        failed_item_ids = []
        for handler in self._handlers:
            response = handler.handle()
            if not response.success:
                failed_item_ids.append(response.item_id)
        response = DynamodbEventBatchResponse(failed_item_ids=failed_item_ids)
        self.__log_on_finish(failed_item_ids)
        return response

    def __log_on_start(self):
        logger.info([
            ("event", "DYNAMODB_EVENT"),
            ("type", "BATCH"),
            ("STATUS", "STARTED"),
            ("batchSize", len(self._handlers)),
        ])

    def __log_on_finish(self, failed_item_ids: List[str]):
        message = [
            ("event", "DYNAMODB_EVENT"),
            ("type", "BATCH"),
        ]

        if not failed_item_ids:
            status = "SUCCESS"
        elif len(failed_item_ids) < len(self._handlers):
            status = "PARTIALLY_FAILED"
        else:
            status = "ALL_FAILED"
        message.append(("STATUS", status))
        if failed_item_ids:
            message.append(("failedItemIDs", failed_item_ids))

        logger.info(message)


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
