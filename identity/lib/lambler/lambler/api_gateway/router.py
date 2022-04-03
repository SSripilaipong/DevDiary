from http import HTTPStatus

from typing import Dict, Optional, List, Iterator, Any, TYPE_CHECKING
import bisect
import pydantic

from lambler.api_gateway.aws.event_v2 import AWSAPIGatewayEventV2
from lambler.api_gateway.aws.version import AWSEventVersion
from lambler.api_gateway.endpoint import HTTPEndpoint
from lambler.api_gateway.endpoint.exception import InvalidParameterError
from lambler.api_gateway.endpoint.post import PostEndpoint
from lambler.api_gateway.event import APIGatewayEvent
from lambler.api_gateway.method import RequestMethodEnum
from lambler.api_gateway.response import APIGatewayResponse, HTTPResponse, JSONResponse
from lambler.base.handler import Handler
from lambler.base.router import Router


class EndpointSortWrapper:
    def __init__(self, endpoint: HTTPEndpoint):
        self._endpoint = endpoint

    def __eq__(self, other):
        assert isinstance(other, EndpointSortWrapper)
        return self._endpoint.path_length == other._endpoint.path_length

    def __lt__(self, other):
        assert isinstance(other, EndpointSortWrapper)
        return self._endpoint.path_length < other._endpoint.path_length

    def __le__(self, other):
        assert isinstance(other, EndpointSortWrapper)
        return self._endpoint.path_length <= other._endpoint.path_length

    @property
    def endpoint(self):
        return self._endpoint


class APIGatewayEventHandler(Handler):
    def __init__(self, endpoint: HTTPEndpoint, event: APIGatewayEvent):
        self._endpoint = endpoint
        self._event = event

    def handle(self) -> APIGatewayResponse:
        try:
            body = self._endpoint.handle(self._event)
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


class APIGatewayRouter(Router):
    def __init__(self, *, event_version=None):
        self._event_version = _validate_event_version(event_version)
        self._endpoints: List[EndpointSortWrapper] = []

    def _iterate_endpoints(self) -> Iterator[HTTPEndpoint]:
        for wrapper in self._endpoints:
            yield wrapper.endpoint

    def _make_handler(self, endpoint: HTTPEndpoint, event: APIGatewayEvent) -> APIGatewayEventHandler:
        return APIGatewayEventHandler(endpoint, event)

    def _on_no_endpoint_matched(self, event: APIGatewayEvent) -> Optional[Handler]:
        return None

    def get(self, path: str):
        def decorator(func):
            self._append_endpoint(HTTPEndpoint(path, method=RequestMethodEnum.GET, handle=func))
            return func
        return decorator

    def post(self, path: str):
        def decorator(func):
            self._append_endpoint(PostEndpoint(path, method=RequestMethodEnum.POST, handle=func))
            return func
        return decorator

    def _append_endpoint(self, endpoint: HTTPEndpoint):
        bisect.insort_right(self._endpoints, EndpointSortWrapper(endpoint))

    def _validate_event(self, event: Dict) -> Optional[APIGatewayEvent]:
        try:
            if self._event_version is None:
                return APIGatewayEvent(**event)
            if self._event_version == AWSEventVersion.V2:
                return AWSAPIGatewayEventV2(**event).normalize()
        except pydantic.ValidationError:
            return None
        raise NotImplementedError()

    if TYPE_CHECKING:
        def match(self, event: Dict, context: Any) -> Optional[APIGatewayEventHandler]: ...


def _validate_event_version(version: str) -> Optional[AWSEventVersion]:
    if version is None:
        return None

    return AWSEventVersion[version.upper()]
