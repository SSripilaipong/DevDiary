import json

import inspect
from typing import Callable, Dict, Any

from lambler.api_gateway.endpoint import HTTPEndpointPattern
from lambler.api_gateway.endpoint.endpoint import HTTPHandler
from lambler.api_gateway.endpoint.exception import InvalidParameterError
from lambler.api_gateway.event import APIGatewayEvent
from lambler.api_gateway.method import RequestMethodEnum
from lambler.base.marker import Marker


class RequestBodyInjection:
    def __init__(self, markers: Dict[str, Marker]):
        self._markers = markers

    @classmethod
    def from_handle_function(cls, handle: Callable) -> 'RequestBodyInjection':
        signature = inspect.signature(handle)
        markers = {}
        for name, marker in signature.parameters.items():
            type_ = marker.annotation
            value = marker.default
            if isinstance(value, Marker):
                value.register_type(type_)
                markers[name] = value
            else:
                raise NotImplementedError()  # TODO: implement

        return RequestBodyInjection(markers)

    def extract_params(self, event: APIGatewayEvent) -> Dict:
        if not self._markers:
            return {}

        body = self._extract_request_body(event)
        return {key: marker.extract_param(body) for key, marker in self._markers.items()}

    def _extract_request_body(self, event):
        if event.headers.get('content-type', None) != 'application/json':
            raise InvalidParameterError()
        try:
            body = json.loads(event.body)
        except json.JSONDecodeError:
            raise InvalidParameterError()
        if not isinstance(body, dict):
            raise InvalidParameterError()
        return body


class PostHandler(HTTPHandler):
    def __init__(self, handle: Callable, event: APIGatewayEvent, body_injection: RequestBodyInjection):
        super().__init__(handle=handle)
        self._event = event
        self._body_injection = body_injection

    @classmethod
    def create(cls, endpoint: 'HTTPEndpointPattern', handle: Callable, event: APIGatewayEvent) -> 'HTTPHandler':
        return cls(handle, event, RequestBodyInjection.from_handle_function(handle))

    def _execute(self) -> Any:
        return self._handle(**self._body_injection.extract_params(self._event))


class PostEndpointPattern(HTTPEndpointPattern):
    def __init__(self, path: str, method: RequestMethodEnum, handle: Callable):
        super().__init__(path, method, handle)
        self._body_injection = RequestBodyInjection.from_handle_function(handle)

    def _create_handler(self, event: APIGatewayEvent) -> HTTPHandler:
        return PostHandler.create(self, self._handle, event)
