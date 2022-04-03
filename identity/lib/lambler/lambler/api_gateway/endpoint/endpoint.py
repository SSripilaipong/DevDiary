from typing import Callable

from lambler.api_gateway.event import APIGatewayEvent
from lambler.api_gateway.method import RequestMethodEnum
from lambler.base.router.endpoint import Endpoint


class HTTPEndpoint(Endpoint):
    def __init__(self, path: str, method: RequestMethodEnum, handle: Callable):
        self._path = path
        self._method = method
        self._path_length = len(path)
        self._handle = handle

    def can_accept(self, event: APIGatewayEvent) -> bool:
        if event.path == self._path:
            return event.method == self._method
        return False

    def handle(self, event: APIGatewayEvent):
        return self._handle()

    @property
    def path_length(self):
        return self._path_length
