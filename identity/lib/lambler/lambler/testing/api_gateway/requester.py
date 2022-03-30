from typing import Dict

import json

from lambler import Lambler
from lambler.api_gateway.aws.event_v2 import AWSAPIGatewayEventV2
from lambler.api_gateway.aws.version import AWSEventVersion
from lambler.api_gateway.event import APIGatewayEvent
from lambler.api_gateway.method import RequestMethodEnum
from lambler.api_gateway.response import APIGatewayResponse, JSONResponse, HTTPResponse


class HTTPRequester:
    def __init__(self, lambler: Lambler, *, event_version: AWSEventVersion = None):
        self._lambler = lambler
        self._event_version = event_version

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
        event = self.__make_event(path, method, body, headers)
        response = self._lambler(event, ...)
        return self.__convert_response(response)

    def __make_event(self, path: str, method: RequestMethodEnum, body: str, headers: Dict) -> Dict:
        api_event = {
            "path": path,
            "method": method,
            "query_string_parameters": {},
            "headers": headers or {},
            "body": body,
        }
        if self._event_version is None:
            return api_event
        elif self._event_version == AWSEventVersion.V2:
            return AWSAPIGatewayEventV2.from_api_event(APIGatewayEvent(**api_event)).dict(by_alias=True)
        else:
            raise NotImplementedError()

    def __convert_response(self, raw: Dict) -> APIGatewayResponse:
        assert isinstance(raw, dict)

        headers = raw["headers"]
        status_code = raw["statusCode"]

        if headers.get("content-type", None) == "application/json":
            return JSONResponse(body=json.loads(raw.get("body", "null")), status_code=status_code)

        return HTTPResponse(body=raw.get("body", None), status_code=status_code)
