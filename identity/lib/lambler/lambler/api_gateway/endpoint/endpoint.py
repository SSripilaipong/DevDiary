from abc import abstractmethod
from http import HTTPStatus

from typing import Callable, Any, Optional

from lambler.api_gateway.endpoint.exception import InvalidParameterError
from lambler.api_gateway.event import APIGatewayEvent
from lambler.api_gateway.method import RequestMethodEnum
from lambler.api_gateway.response import JSONResponse, HTTPResponse, APIGatewayResponse
from lambler.base.handler import PatternMatcher, Handler
from lambler.base.response import LamblerResponse


class HTTPHandler(Handler):
    def __init__(self, handle: Callable):
        self._handle = handle

    @classmethod
    def create(cls, endpoint: 'HTTPEndpointPattern', handle: Callable, event: APIGatewayEvent) -> 'HTTPHandler':
        return cls(handle)

    def _execute(self) -> Any:
        return self._handle()

    def handle(self) -> LamblerResponse:
        try:
            body = self._execute()
        except InvalidParameterError:
            return JSONResponse({"message": "Unprocessable Entity"}, status_code=HTTPStatus.UNPROCESSABLE_ENTITY)
        except BaseException:
            return JSONResponse({"message": "Internal Server Error"}, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
        if body is None:
            return HTTPResponse("", HTTPStatus.OK)
        elif isinstance(body, str):
            return HTTPResponse(body, HTTPStatus.OK)
        elif isinstance(body, dict):
            return JSONResponse(body, HTTPStatus.OK)
        elif isinstance(body, APIGatewayResponse):
            return body
        else:
            raise NotImplementedError()


class HTTPPathPattern(PatternMatcher):
    @property
    @abstractmethod
    def path_length(self) -> int:
        pass


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
        return HTTPHandler.create(self, self._handle, event)
