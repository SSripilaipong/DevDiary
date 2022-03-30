from lambler import Lambler
from lambler.api_gateway.method import RequestMethodEnum
from lambler.api_gateway.response import APIGatewayResponse


class HTTPRequester:
    def __init__(self, lambler: Lambler):
        self._lambler = lambler

    def get(self, path: str) -> APIGatewayResponse:
        return self.__call_lambler(path, RequestMethodEnum.GET)

    def post(self, path: str) -> APIGatewayResponse:
        return self.__call_lambler(path, RequestMethodEnum.POST)

    def __call_lambler(self, path: str, method: RequestMethodEnum) -> APIGatewayResponse:
        event = {
            "path": path,
            "method": method,
            "query_string_parameters": {},
            "headers": {},
            "body": "",
        }
        return self._lambler.call_raw_response(event, ...)
