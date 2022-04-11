from lambler.base.function.input import FunctionInputSource
from lambler.dynamodb_event.data.event import DynamodbEvent


class DynamodbEventItemIdInputSource(FunctionInputSource):
    def __init__(self, id_: str):
        self._id = id_

    @classmethod
    def from_event(cls, event: DynamodbEvent) -> 'DynamodbEventItemIdInputSource':
        return cls(event.event_id)

    def to_str(self) -> str:
        return self._id
