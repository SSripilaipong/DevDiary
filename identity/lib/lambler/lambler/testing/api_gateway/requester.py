from lambler import Lambler
from lambler.api_gateway.method import RequestMethodEnum
from lambler.api_gateway.status import HTTPStatus
from lambler.api_gateway.response import JSONResponse, APIGatewayResponse


class HTTPRequester:
    def __init__(self, lambler: Lambler):
        self._lambler = lambler

    def get(self, path: str) -> APIGatewayResponse:
        event = {
            "path": path,
            "method": RequestMethodEnum.GET,
            "query_string_parameters": {},
            "headers": {},
            "body": "",
        }
        return self._lambler.call_raw_response(event, ...)

    def post(self, path: str) -> APIGatewayResponse:
        pass
