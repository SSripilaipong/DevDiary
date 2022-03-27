from typing import Dict, Any

from lambler.api_gateway.endpoint.base import Endpoint
from lambler.api_gateway.event import ApiGatewayEvent
from lambler.base.handler import HandlerMatcher


class APIGatewayRouter(HandlerMatcher):
    def __init__(self, endpoint_mapper: Dict[str, Endpoint] = None, default_endpoint: Endpoint = None):
        self._endpoint_mapper = endpoint_mapper
        self._default_endpoint = default_endpoint

    def _get_endpoint(self, route_key: str) -> Endpoint:
        return self._endpoint_mapper.get(route_key, self._default_endpoint)

    def handle(self, raw_event: Dict) -> Any:
        event = ApiGatewayEvent(**raw_event)
        route_key = self.extract_route_key(event)
        endpoint = self._get_endpoint(route_key)
        return endpoint.process(event.headers, event.query_string_parameters, event.body)

    @classmethod
    def match(cls, event: Dict, context: Any) -> bool:
        pass

    def extract_route_key(self, event: ApiGatewayEvent) -> str:
        pass
