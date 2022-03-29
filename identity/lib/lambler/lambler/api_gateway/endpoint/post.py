import json

import inspect
import pydantic
from pydantic import BaseModel

from typing import Callable, Any, Dict

import chamber.data.exception
from chamber.data.model import DataModel
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
                if annotation is dict or annotation is Dict:
                    params[name] = dict
                elif isinstance(annotation, type) and issubclass(annotation, BaseModel):
                    params[name] = annotation
                elif isinstance(annotation, type) and issubclass(annotation, DataModel):
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
            raise InvalidParameterError()

        if not isinstance(body, dict):
            raise InvalidParameterError()

        params = {}
        for key, type_ in self._params.items():
            if type_ is dict:
                params[key] = body
            elif isinstance(type_, type) and issubclass(type_, BaseModel):
                try:
                    params[key] = type_(**body)
                except pydantic.ValidationError:
                    raise InvalidParameterError()
            elif isinstance(type_, type) and issubclass(type_, DataModel):
                try:
                    params[key] = type_.from_dict(body)
                except chamber.data.exception.DeserializationFailedException:
                    raise InvalidParameterError()
            else:
                raise NotImplementedError()

        return params


class PostEndpoint(Endpoint):
    def __init__(self, path: str, method: RequestMethodEnum, handle: Callable):
        super().__init__(path, method, handle)
        self._body_injection = RequestBodyInjection.from_handle_function(handle)

    def handle(self, event: APIGatewayEvent):
        return self._handle(**self._body_injection.extract_params(event))
