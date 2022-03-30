import json

from lambler import Lambler
from lambler.api_gateway.method import RequestMethodEnum
from lambler.api_gateway.status import HTTPStatus
from lambler.testing.api_gateway.response import HTTPResponse


class HTTPRequester:
    def __init__(self, lambler: Lambler):
        self._lambler = lambler

    def get(self, path: str) -> HTTPResponse:
        event = {
            "path": path,
            "method": RequestMethodEnum.GET,
            "query_string_parameters": {},
            "headers": {},
            "body": "",
        }
        payload = self._lambler(event, ...)
        return HTTPResponse(json.dumps(payload), HTTPStatus.OK)
