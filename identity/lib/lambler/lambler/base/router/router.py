from abc import abstractmethod

from typing import Dict, Any, Optional, Iterator

from lambler.base.event import LamblerEvent
from lambler.base.handler import PatternMatcher, Handler


class Router(PatternMatcher):
    @abstractmethod
    def _iterate_patterns(self) -> Iterator[PatternMatcher]:
        pass

    @abstractmethod
    def _validate_event(self, event: Dict) -> Optional[LamblerEvent]:
        pass

    @abstractmethod
    def _on_no_pattern_matched(self, event: LamblerEvent) -> Optional[Handler]:
        pass

    def match(self, event: Dict, context: Any) -> Optional[Handler]:
        validated_event = self._validate_event(event)
        if validated_event is None:
            return None
        return self.__match_handler_from_endpoints(validated_event, context)

    def __match_handler_from_endpoints(self, event: LamblerEvent, context: Any) -> Optional[Handler]:
        for pattern in self._iterate_patterns():
            handler = pattern.match(event, context)
            if handler is not None:
                return handler
        return None
