import inspect

from typing import Callable, Dict

from boto3.dynamodb.types import TypeDeserializer

from lambler.base.marker import Marker
from lambler.base.router.endpoint import Endpoint
from lambler.dynamodb_event.event import DynamodbEvent
from lambler.dynamodb_event.response import DynamodbEventResponse
from lambler.dynamodb_event.type import DynamodbEventType


class ParameterInjection:
    def __init__(self, markers: Dict[str, Marker]):
        self._markers = markers
        self._deserializer = TypeDeserializer()

    @classmethod
    def from_handle_function(cls, handle: Callable) -> 'ParameterInjection':
        markers = {}
        for name, parameter in inspect.signature(handle).parameters.items():
            value = parameter.default
            if isinstance(value, Marker):
                value.register_type(parameter.annotation)
                markers[name] = value
            else:
                raise NotImplementedError()
        return cls(markers)

    def extract_params(self, event: DynamodbEvent) -> Dict:
        if self._markers == {}:
            return {}

        body = event.dynamodb.new_image or {}
        body = {key: self._deserializer.deserialize(value) for key, value in body.items()}
        return {key: marker.extract_param(body) for key, marker in self._markers.items()}


class DynamodbEventEndpoint(Endpoint):
    def __init__(self, method: DynamodbEventType, handle: Callable):
        self._method = method
        self._handle = handle

        self._param_injection = ParameterInjection.from_handle_function(handle)

    def can_accept(self, event: DynamodbEvent) -> bool:
        return True

    def process(self, event: DynamodbEvent) -> DynamodbEventResponse:
        params = self._param_injection.extract_params(event)
        self._handle(**params)
        return DynamodbEventResponse()
