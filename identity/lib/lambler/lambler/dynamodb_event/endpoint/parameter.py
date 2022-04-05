import inspect

from boto3.dynamodb.types import TypeDeserializer
from typing import Dict, Callable

from lambler.base.marker import Marker
from lambler.dynamodb_event.model.event import DynamodbEvent


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
