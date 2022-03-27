from typing import Dict, Any, Optional
import pydantic

from lambler.api_gateway.event import APIGatewayEvent
from lambler.base.handler import HandlerMatcher, Handler


class APIGatewayRouter(HandlerMatcher):
    def handle(self, raw_event: Dict) -> Any:
        event = APIGatewayEvent(**raw_event)
        route_key = self.extract_route_key(event)
        endpoint = self._get_endpoint(route_key)
        return endpoint.process(event.headers, event.query_string_parameters, event.body)

    def match(self, event: Dict, context: Any) -> Optional[Handler]:
        try:
            APIGatewayEvent(**event)
        except pydantic.ValidationError:
            return None
        return APIGatewayEventHandler()

    def get(self, path: str):
        return lambda func: ...


class APIGatewayEventHandler(Handler):
    def handle(self) -> Any:
        pass
