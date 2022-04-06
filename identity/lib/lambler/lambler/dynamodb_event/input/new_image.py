from boto3.dynamodb.types import TypeDeserializer
from typing import Dict

from lambler.base.function.input import FunctionInputSource
from lambler.dynamodb_event.data.event import DynamodbEvent


class DynamodbEventNewImageInputSource(FunctionInputSource):
    def __init__(self, data: Dict):
        self._data = data
        self._deserializer = TypeDeserializer()

    @classmethod
    def from_event(cls, event: DynamodbEvent) -> 'DynamodbEventNewImageInputSource':
        return cls(event.dynamodb.new_image)

    def to_dict(self) -> Dict:
        return {key: self._deserializer.deserialize(value) for key, value in self._data.items()}
