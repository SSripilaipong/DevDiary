from typing import Dict, Any

from api_gateway.endpoint import Endpoint
from api_gateway.service_event import ApiGatewayServiceEvent
from lambda_handler.service_event.handler import ServiceEventHandler


class ApiGatewayServiceEventHandler(ServiceEventHandler):
    def __init__(self, endpoint_mapper: Dict[str, Endpoint], default_endpoint: Endpoint = None):
        self._endpoint_mapper = endpoint_mapper
        self._default_endpoint = default_endpoint

    def _get_endpoint(self, route_key: str) -> Endpoint:
        return self._endpoint_mapper.get(route_key, self._default_endpoint)

    def handle(self, raw_event: Dict) -> Any:
        event = ApiGatewayServiceEvent(**raw_event)
        route_key = self._extract_route_key(event)
        endpoint = self._get_endpoint(route_key)
        return endpoint.process(event.headers, event.query_string_parameters, event.body)

    @classmethod
    def match(cls, raw_event: Dict) -> bool:
        return raw_event.get('headers', {}).get('x-service-endpoint', None) is not None

    @staticmethod
    def _extract_route_key(event: ApiGatewayServiceEvent):
        return event.headers['x-service-endpoint']
