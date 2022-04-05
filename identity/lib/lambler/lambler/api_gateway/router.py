from typing import Dict, Optional, List, Iterator, Any, TYPE_CHECKING
import bisect
import pydantic

from lambler.api_gateway.aws.event_v2 import AWSAPIGatewayEventV2
from lambler.api_gateway.aws.version import AWSEventVersion
from lambler.api_gateway.endpoint import HTTPEndpointPattern
from lambler.api_gateway.endpoint.endpoint import HTTPHandler, HTTPPathPattern
from lambler.api_gateway.endpoint.post import PostEndpointPattern
from lambler.api_gateway.event import APIGatewayEvent
from lambler.api_gateway.method import RequestMethodEnum
from lambler.base.handler import Handler
from lambler.base.router import Router


class PathPatternSortWrapper:
    def __init__(self, pattern: HTTPPathPattern):
        self._pattern = pattern

    def __eq__(self, other):
        assert isinstance(other, PathPatternSortWrapper)
        return self._pattern.path_length == other._pattern.path_length

    def __lt__(self, other):
        assert isinstance(other, PathPatternSortWrapper)
        return self._pattern.path_length < other._pattern.path_length

    def __le__(self, other):
        assert isinstance(other, PathPatternSortWrapper)
        return self._pattern.path_length <= other._pattern.path_length

    @property
    def pattern(self) -> HTTPPathPattern:
        return self._pattern


class APIGatewayRouter(Router):
    def __init__(self, *, event_version=None):
        self._event_version = _validate_event_version(event_version)
        self._endpoints: List[PathPatternSortWrapper] = []

    def _iterate_patterns(self) -> Iterator[HTTPPathPattern]:
        for wrapper in self._endpoints:
            yield wrapper.pattern

    def _on_no_pattern_matched(self, event: APIGatewayEvent) -> Optional[Handler]:
        return None

    def get(self, path: str):
        def decorator(func):
            self._append_pattern(HTTPEndpointPattern(path, method=RequestMethodEnum.GET, handle=func))
            return func
        return decorator

    def post(self, path: str):
        def decorator(func):
            self._append_pattern(PostEndpointPattern(path, method=RequestMethodEnum.POST, handle=func))
            return func
        return decorator

    def _append_pattern(self, pattern: HTTPPathPattern):
        bisect.insort_right(self._endpoints, PathPatternSortWrapper(pattern))

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
        def match(self, event: Dict, context: Any) -> Optional[HTTPHandler]: ...


def _validate_event_version(version: str) -> Optional[AWSEventVersion]:
    if version is None:
        return None

    return AWSEventVersion[version.upper()]
