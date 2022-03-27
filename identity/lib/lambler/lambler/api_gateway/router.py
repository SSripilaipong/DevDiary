from typing import Dict, Any, Optional, List, Tuple
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
    def __init__(self):
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
        def decorator(func):
            endpoint = Endpoint(path, method=RequestMethodEnum.GET, handle=func)
            bisect.insort_right(self._endpoints, EndpointSortWrapper(endpoint))
            return func
        return decorator


class APIGatewayEventHandler(Handler):
    def __init__(self, endpoint: Endpoint, event: APIGatewayEvent):
        self._endpoint = endpoint
        self._event = event

    def handle(self) -> Any:
        self._endpoint.handle(self._event)
