import json

import inspect

from typing import Callable, Any, Dict

from lambler.api_gateway.endpoint import Endpoint
from lambler.api_gateway.endpoint.exception import InvalidParameterError
from lambler.api_gateway.endpoint.marker import JSONBody
from lambler.api_gateway.event import APIGatewayEvent
from lambler.api_gateway.method import RequestMethodEnum


class RequestBodyInjection:
    def __init__(self, params: Dict):
        self._params = params

    @classmethod
    def from_handle_function(cls, handle: Callable) -> 'RequestBodyInjection':
        signature = inspect.signature(handle)
        params = {}
        for name, param in signature.parameters.items():
            annotation = param.annotation
            default = param.default
            if isinstance(default, type) and issubclass(default, JSONBody):
                default = default()
            if isinstance(default, JSONBody):
                if annotation == dict:
                    params[name] = annotation
                else:
                    raise NotImplementedError()  # TODO: implement this

        return RequestBodyInjection(params)

    def extract_params(self, event: APIGatewayEvent) -> Dict:
        if not self._params:
            return {}

        if event.headers.get('content-type', None) != 'application/json':
            raise InvalidParameterError()

        try:
            body = json.loads(event.body)
        except json.JSONDecodeError:
            raise NotImplementedError()  # TODO: implement this

        params = {}
        for key, type_ in self._params.items():
            if type_ is dict:
                params[key] = body
            else:
                raise NotImplementedError()

        return params


class PostEndpoint(Endpoint):
    def __init__(self, path: str, method: RequestMethodEnum, handle: Callable):
        super().__init__(path, method, handle)
        self._body_injection = RequestBodyInjection.from_handle_function(handle)

    def handle(self, event: APIGatewayEvent):
        self._handle(**self._body_injection.extract_params(event))
