import inspect

from typing import Callable, Dict, Any, Optional

from boto3.dynamodb.types import TypeDeserializer

from lambler.base.handler import PatternMatcher, Handler
from lambler.base.marker import Marker
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


class DynamodbEventHandler(Handler):
    def __init__(self, handle: Callable, event: DynamodbEvent, param_injection: ParameterInjection):
        self._handle = handle
        self._event = event

        self._param_injection = param_injection

    @classmethod
    def create(cls, method: DynamodbEventType, handle: Callable, event: DynamodbEvent) -> 'DynamodbEventHandler':
        return cls(handle, event, ParameterInjection.from_handle_function(handle))

    def handle(self) -> DynamodbEventResponse:
        params = self._param_injection.extract_params(self._event)
        self._handle(**params)
        return DynamodbEventResponse()


class DynamodbEventEndpoint(PatternMatcher):
    def __init__(self, method: DynamodbEventType, handle: Callable):
        self._method = method
        self._handle = handle

    def match(self, event: DynamodbEvent, context: Any) -> Optional[DynamodbEventHandler]:
        return DynamodbEventHandler.create(self._method, self._handle, event)
