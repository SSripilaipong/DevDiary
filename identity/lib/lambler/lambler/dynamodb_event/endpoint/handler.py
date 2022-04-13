import traceback

from lambler import logger
from lambler.base.function import MarkedFunction
from lambler.base.handler import Handler
from lambler.dynamodb_event.input.collection import DynamodbEventInputCollection
from lambler.dynamodb_event.response import DynamodbEventResponse
from lambler.dynamodb_event.data.type import DynamodbEventType


class DynamodbEventHandler(Handler):
    def __init__(self, handle: MarkedFunction, sources: DynamodbEventInputCollection):
        self._handle = handle
        self._sources = sources

        self._item_id = self._sources.item_id.to_str()
        self._event_type = "INSERT"  # TODO: fix this

    @classmethod
    def create(cls, method: DynamodbEventType, handle: MarkedFunction, sources: DynamodbEventInputCollection) \
            -> 'DynamodbEventHandler':
        return cls(handle, sources)

    def handle(self) -> DynamodbEventResponse:
        self.__log_on_start()
        try:
            self._handle.execute(self._sources)
        except Exception as e:
            print(traceback.format_exc())  # TODO: use log level: DEBUG instead
            response = DynamodbEventResponse(self._item_id, success=False)
            exception = e
        else:
            response = DynamodbEventResponse(self._item_id, success=True)
            exception = None
        self.__log_on_finish(exception)
        return response

    def __log_on_start(self):
        logger.info([
            ("event", "DYNAMODB_EVENT"),
            ("type", self._event_type),
            ("itemId", self._item_id),
            ("status", "STARTED"),
        ])

    def __log_on_finish(self, exception: Exception):
        message = [
            ("event", "DYNAMODB_EVENT"),
            ("type", self._event_type),
            ("itemId", self._item_id),
        ]
        if exception is None:
            message.append(("status", "SUCCESS"))
        else:
            message.append(("status", "FAILED"))
            message.append(("exceptionType", exception.__class__.__name__))
            message.append(("exceptionMessage", str(exception)))
        logger.error(message)
