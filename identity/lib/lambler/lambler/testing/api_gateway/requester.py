from typing import Dict

import json

from lambler import Lambler
from lambler.api_gateway.method import RequestMethodEnum
from lambler.api_gateway.response import APIGatewayResponse, JSONResponse, HTTPResponse


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
        response = self._lambler(event, ...)
        return self.__convert_response(response)

    def __convert_response(self, raw: Dict) -> APIGatewayResponse:
        assert isinstance(raw, dict)

        headers = raw["headers"]
        status_code = raw["statusCode"]

        if headers.get("content-type", None) == "application/json":
            return JSONResponse(body=json.loads(raw.get("body", "null")), status_code=status_code)

        return HTTPResponse(body=raw.get("body", None), status_code=status_code)
