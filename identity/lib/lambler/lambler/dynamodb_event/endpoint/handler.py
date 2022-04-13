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

    @classmethod
    def create(cls, method: DynamodbEventType, handle: MarkedFunction, sources: DynamodbEventInputCollection) \
            -> 'DynamodbEventHandler':
        return cls(handle, sources)

    def handle(self) -> DynamodbEventResponse:
        try:
            self._handle.execute(self._sources)
        except:
            return DynamodbEventResponse(self._item_id, success=False)
        return DynamodbEventResponse(self._item_id, success=True)
