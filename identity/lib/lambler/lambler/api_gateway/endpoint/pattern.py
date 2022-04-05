from typing import Callable, Any, Optional

from lambler.api_gateway.endpoint.abstract import HTTPPathPattern
from lambler.api_gateway.endpoint.handler import HTTPHandler
from lambler.api_gateway.event import APIGatewayEvent
from lambler.api_gateway.method import RequestMethodEnum


class HTTPEndpointPattern(HTTPPathPattern):
    def __init__(self, path: str, method: RequestMethodEnum, handle: Callable):
        self._path = path
        self._method = method
        self._path_length = len(path)
        self._handle = handle

    def match(self, event: Any, context: Any) -> Optional[HTTPHandler]:
        assert isinstance(event, APIGatewayEvent)
        if event.path == self._path and event.method == self._method:
            return self._create_handler(event)
        return None

    @property
    def path_length(self) -> int:
        return self._path_length

    def _create_handler(self, event: APIGatewayEvent) -> HTTPHandler:
        return HTTPHandler.create(self._handle, event)
