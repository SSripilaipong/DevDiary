from typing import Callable, Any

from lambler.api_gateway.event import APIGatewayEvent
from lambler.api_gateway.response import response_parser
from lambler.base.handler import Handler
from lambler.base.response import LamblerResponse


class HTTPHandler(Handler):
    def __init__(self, handle: Callable):
        self._handle = handle

    @classmethod
    def create(cls, handle: Callable, event: APIGatewayEvent) -> 'HTTPHandler':
        return cls(handle)

    def _execute(self) -> Any:
        return self._handle()

    def handle(self) -> LamblerResponse:
        try:
            body = self._execute()
        except BaseException as e:
            return response_parser.parse_error(e)

        return response_parser.parse_response(body)
