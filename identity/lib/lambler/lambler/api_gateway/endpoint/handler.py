from typing import Any

from lambler.api_gateway.endpoint.input import HTTPInputCollection
from lambler.base.function import MarkedFunction
from lambler.base.function.input import FunctionInputSourceCollection
from lambler.api_gateway.event import APIGatewayEvent
from lambler.api_gateway.response import response_parser
from lambler.base.handler import Handler
from lambler.base.response import LamblerResponse


class HTTPHandler(Handler):
    def __init__(self, handle: MarkedFunction, sources: FunctionInputSourceCollection):
        self._handle = handle
        self._sources = sources

    @classmethod
    def create(cls, handle: MarkedFunction, event: APIGatewayEvent) -> 'HTTPHandler':
        return cls(handle, HTTPInputCollection.from_event(event))

    def _execute(self) -> Any:
        return self._handle.execute(self._sources)

    def handle(self) -> LamblerResponse:
        try:
            body = self._execute()
        except BaseException as e:
            return response_parser.parse_error(e)

        return response_parser.parse_response(body)
