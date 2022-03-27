from typing import Dict, Any, Optional, List
import bisect
import pydantic

from lambler.api_gateway.aws.event_v2 import AWSAPIGatewayEventV2
from lambler.api_gateway.aws.version import AWSEventVersion
from lambler.api_gateway.endpoint import Endpoint
from lambler.api_gateway.endpoint.post import PostEndpoint
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
        self._event_version = _validate_event_version(event_version)
        self._endpoints: List[EndpointSortWrapper] = []

    def match(self, event: Dict, context: Any) -> Optional[Handler]:
        api_event = self._validate_event(event)
        return self._match_event_with_endpoints(api_event)

    def _match_event_with_endpoints(self, api_event):
        for wrapper in self._endpoints:
            endpoint = wrapper.endpoint
            if endpoint.match(api_event):
                return APIGatewayEventHandler(endpoint, api_event)
        return None

    def get(self, path: str):
        def decorator(func):
            self._append_endpoint(Endpoint(path, method=RequestMethodEnum.GET, handle=func))
            return func
        return decorator

    def post(self, path: str):
        def decorator(func):
            self._append_endpoint(PostEndpoint(path, method=RequestMethodEnum.POST, handle=func))
            return func
        return decorator

    def _append_endpoint(self, endpoint: Endpoint):
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


class APIGatewayEventHandler(Handler):
    def __init__(self, endpoint: Endpoint, event: APIGatewayEvent):
        self._endpoint = endpoint
        self._event = event

    def handle(self) -> Any:
        self._endpoint.handle(self._event)


def _validate_event_version(version: str) -> Optional[AWSEventVersion]:
    if version is None:
        return None

    return AWSEventVersion[version.upper()]
