from typing import Dict, Any

from app import dependency
from app.api.handler import get_api_gateway_handler
from lambler.base.handler import HandlerMatcher
from lambler.base.handler.mapper import ServiceEventHandlerMapper


class PrintEventHandler(HandlerMatcher):

    @classmethod
    def match(cls, raw_event: Dict) -> bool:
        return True

    def handle(self, raw_event: Dict) -> Any:
        print(raw_event)


event_handler_mapper = ServiceEventHandlerMapper.from_list([
    get_api_gateway_handler(),
    PrintEventHandler(),
])


dependency.inject()


def handler(event, _):
    event_handler = event_handler_mapper.map(event)
    return event_handler.handle(event)
