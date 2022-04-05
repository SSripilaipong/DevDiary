from http import HTTPStatus

from typing import Any

from lambler.api_gateway.exception import InvalidParameterError
from lambler.api_gateway.response import APIGatewayResponse, HTTPResponse, JSONResponse


class ResponseParser:
    def parse_error(self, error: BaseException) -> APIGatewayResponse:
        if isinstance(error, InvalidParameterError):
            return JSONResponse({"message": "Unprocessable Entity"}, status_code=HTTPStatus.UNPROCESSABLE_ENTITY)
        return JSONResponse({"message": "Internal Server Error"}, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

    def parse_response(self, raw: Any) -> APIGatewayResponse:
        if raw is None:
            return HTTPResponse("", HTTPStatus.OK)
        elif isinstance(raw, str):
            return HTTPResponse(raw, HTTPStatus.OK)
        elif isinstance(raw, dict):
            return JSONResponse(raw, HTTPStatus.OK)
        elif isinstance(raw, APIGatewayResponse):
            return raw
        else:
            raise NotImplementedError()


response_parser = ResponseParser()
