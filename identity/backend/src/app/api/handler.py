from typing import Dict

from lambler.api_gateway.handler import ApiGatewayServiceEventHandler
from lambler.api_gateway.service_event import ApiGatewayServiceEvent
from app.api.endpoint.default import AlwaysOkEndpoint
from app.api.endpoint.register import RegisterEndpoint


class MyApiGatewayServiceEventHandler(ApiGatewayServiceEventHandler):
    @classmethod
    def match(cls, raw_event: Dict) -> bool:
        return raw_event.get('headers', {}).get('x-service-endpoint', None) is not None

    def extract_route_key(self, event: ApiGatewayServiceEvent) -> str:
        return event.headers['x-service-endpoint']


def get_api_gateway_handler() -> MyApiGatewayServiceEventHandler:
    return MyApiGatewayServiceEventHandler({
        "IdentityRegister": RegisterEndpoint(),
    }, default_endpoint=AlwaysOkEndpoint())
