import inspect

from typing import Callable, Dict

from boto3.dynamodb.types import TypeDeserializer

from lambler.base.router.endpoint import Endpoint
from lambler.dynamodb_event.event import DynamodbEvent
from lambler.dynamodb_event.marker import EventBody
from lambler.dynamodb_event.response import DynamodbEventResponse
from lambler.dynamodb_event.type import DynamodbEventType


class DynamodbEventEndpoint(Endpoint):
    def __init__(self, method: DynamodbEventType, handle: Callable):
        self._method = method
        self._handle = handle

        self._parameters = inspect.signature(self._handle).parameters
        self._deserializer = TypeDeserializer()

    def can_accept(self, event: DynamodbEvent) -> bool:
        return True

    def process(self, event: DynamodbEvent) -> DynamodbEventResponse:
        params = self._extract_params(event)
        self._handle(**params)
        return DynamodbEventResponse()

    def _extract_params(self, event: DynamodbEvent) -> Dict:
        body = event.dynamodb.new_image or {}
        body = {key: self._deserializer.deserialize(value) for key, value in body.items()}

        params = {}
        for name, marker in self._parameters.items():
            if isinstance(marker.default, EventBody):
                params[name] = body
            else:
                raise NotImplementedError()

        return params
