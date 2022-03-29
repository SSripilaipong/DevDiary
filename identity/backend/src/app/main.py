from typing import Dict, Any

from app import dependency
from app.api.router import router
from lambler import Lambler
from lambler.base.handler import PatternMatcher, Handler


dependency.inject()


class PrintEventHandler(PatternMatcher, Handler):
    def __init__(self, value=None):
        self._value = value

    def match(self, event: Dict, context: Any) -> Handler:
        return PrintEventHandler(event)

    def handle(self) -> Any:
        print(self._value)


handler = Lambler()
handler.include_pattern(router)
handler.include_pattern(PrintEventHandler())
