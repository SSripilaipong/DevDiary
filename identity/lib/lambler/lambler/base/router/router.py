from abc import abstractmethod

from typing import Dict, Any, Optional, Iterator

from lambler.base.event import LamblerEvent
from lambler.base.handler import PatternMatcher, Handler
from lambler.base.router.endpoint import Endpoint


class Router(PatternMatcher):
    @abstractmethod
    def _iterate_endpoints(self) -> Iterator[Endpoint]:
        pass

    @abstractmethod
    def _make_handler(self, endpoint: Endpoint, event: LamblerEvent) -> Handler:
        pass

    @abstractmethod
    def _validate_event(self, event: Dict) -> Optional[LamblerEvent]:
        pass

    @abstractmethod
    def _on_no_endpoint_matched(self, event: LamblerEvent) -> Optional[Handler]:
        pass

    def match(self, event: Dict, context: Any) -> Optional[Handler]:
        validated_event = self._validate_event(event)
        if validated_event is None:
            return None
        endpoint = self.__match_event_with_endpoints(validated_event)
        if endpoint is None:
            return self._on_no_endpoint_matched(validated_event)
        return self._make_handler(endpoint, validated_event)

    def __match_event_with_endpoints(self, event: LamblerEvent) -> Optional[Endpoint]:
        for endpoint in self._iterate_endpoints():
            if endpoint.can_accept(event):
                return endpoint
        return None
