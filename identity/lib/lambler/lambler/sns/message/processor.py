from typing import Any, Optional, TypeVar, Callable

from lambler.base.handler import PatternMatcher, Handler


T = TypeVar("T", bound=Callable)


class SNSMessageProcessor(PatternMatcher):
    def match(self, event: Any, context: Any) -> Optional[Handler]:
        pass

    def message(self):
        def decorator(func: T) -> T:
            pass
        return decorator
