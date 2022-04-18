from typing import Any, Optional, Callable

from lambler.base.handler import PatternMatcher
from lambler.sns.message.handler import SNSMessageHandler


class SNSMessageEndpoint(PatternMatcher):
    def __init__(self, handle: Callable):
        self._handle = handle

    def match(self, event: Any, context: Any) -> Optional[SNSMessageHandler]:
        return SNSMessageHandler(self._handle)
