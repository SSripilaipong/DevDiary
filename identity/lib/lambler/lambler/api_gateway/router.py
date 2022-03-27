from typing import Dict, Any, Optional, List
import bisect
import pydantic

from lambler.api_gateway.endpoint import Endpoint
from lambler.api_gateway.event import APIGatewayEvent
from lambler.api_gateway.method import RequestMethodEnum
from lambler.base.handler import HandlerMatcher, Handler


class EndpointSortWrapper:
    def __init__(self, endpoint: Endpoint):
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


class APIGatewayRouter(HandlerMatcher):
    def __init__(self, *, event_version=None):
        self._endpoints: List[EndpointSortWrapper] = []

    def match(self, event: Dict, context: Any) -> Optional[Handler]:
        try:
            api_event = APIGatewayEvent(**event)
        except pydantic.ValidationError:
            return None
        for wrapper in self._endpoints:
            endpoint = wrapper.endpoint
            if endpoint.match(api_event):
                return APIGatewayEventHandler(endpoint, api_event)
        return None

    def get(self, path: str):
        return self._request_decorator(path, method=RequestMethodEnum.GET)

    def post(self, path: str):
        return self._request_decorator(path, method=RequestMethodEnum.POST)

    def _request_decorator(self, path, method: RequestMethodEnum):
        def decorator(func):
            self._append_endpoint(Endpoint(path, method=method, handle=func))
            return func
        return decorator

    def _append_endpoint(self, endpoint: Endpoint):
        bisect.insort_right(self._endpoints, EndpointSortWrapper(endpoint))


class APIGatewayEventHandler(Handler):
    def __init__(self, endpoint: Endpoint, event: APIGatewayEvent):
        self._endpoint = endpoint
        self._event = event

    def handle(self) -> Any:
        self._endpoint.handle(self._event)
