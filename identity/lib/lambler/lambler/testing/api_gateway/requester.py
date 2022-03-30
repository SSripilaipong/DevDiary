from typing import Dict

import json

from lambler import Lambler
from lambler.api_gateway.method import RequestMethodEnum
from lambler.api_gateway.response import APIGatewayResponse


class HTTPRequester:
    def __init__(self, lambler: Lambler):
        self._lambler = lambler

    def get(self, path: str) -> APIGatewayResponse:
        return self.__call_lambler(path, RequestMethodEnum.GET)

    def post(self, path: str, body: Dict = None) -> APIGatewayResponse:
        if body is None:
            body = ""
            headers = {}
        elif isinstance(body, dict):
            body = json.dumps(body)
            headers = {"content-type": "application/json"}
        else:
            raise NotImplementedError()

        return self.__call_lambler(path, RequestMethodEnum.POST, body=body, headers=headers)

    def __call_lambler(self, path: str, method: RequestMethodEnum, body: str = "",
                       headers: Dict = None) -> APIGatewayResponse:
        event = {
            "path": path,
            "method": method,
            "query_string_parameters": {},
            "headers": headers or {},
            "body": body,
        }
        return self._lambler.call_raw_response(event, ...)
