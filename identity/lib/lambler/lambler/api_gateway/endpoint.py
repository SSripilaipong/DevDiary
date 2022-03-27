from typing import Callable

from lambler.api_gateway.event import APIGatewayEvent
from lambler.api_gateway.method import RequestMethodEnum


class Endpoint:
    def __init__(self, path: str, method: RequestMethodEnum, handle: Callable):
        self._method = method
        self._path_length = len(path)
        self._handle = handle

    def match(self, event: APIGatewayEvent):
        if event.request_context.http.method == self._method:
            return True
        return False

    def handle(self, event: APIGatewayEvent):
        self._handle()

    @property
    def path_length(self):
        return self._path_length
