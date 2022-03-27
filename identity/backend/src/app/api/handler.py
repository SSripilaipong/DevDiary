from typing import Dict, Any

from lambler.api_gateway.handler import APIGatewayRouter
from lambler.api_gateway.event import ApiGatewayEvent
from app.api.endpoint.default import AlwaysOkEndpoint
from app.api.endpoint.register import RegisterEndpoint


class MyApiGatewayServiceEventHandler(APIGatewayRouter):
    @classmethod
    def match(cls, event: Dict, context: Any) -> bool:
        return event.get('headers', {}).get('x-service-endpoint', None) is not None

    def extract_route_key(self, event: ApiGatewayEvent) -> str:
        return event.headers['x-service-endpoint']


def get_api_gateway_handler() -> MyApiGatewayServiceEventHandler:
    return MyApiGatewayServiceEventHandler({
        "IdentityRegister": RegisterEndpoint(),
    }, default_endpoint=AlwaysOkEndpoint())
