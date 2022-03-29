from typing import Dict, Any

from app import dependency
from app.api.router import router
from lambler.base.handler import HandlerMatcher, Handler
from lambler.base.handler.router import HandlerRouter


class PrintEventHandler(HandlerMatcher, Handler):
    def __init__(self, value=None):
        self._value = value

    def match(self, event: Dict, context: Any) -> Handler:
        return PrintEventHandler(event)

    def handle(self) -> Any:
        print(self._value)


event_handler_mapper = HandlerRouter.from_list([
    router,
    PrintEventHandler(),
])


dependency.inject()


def handler(event, context):
    event_handler = event_handler_mapper.match(event, context)
    return event_handler.handle()
