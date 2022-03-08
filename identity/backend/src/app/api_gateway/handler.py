from api_gateway.handler import ApiGatewayServiceEventHandler
from app.api_gateway.endpoint.default import AlwaysOkEndpoint
from app.api_gateway.endpoint.register import RegisterEndpoint


def get_api_gateway_handler() -> ApiGatewayServiceEventHandler:
    return ApiGatewayServiceEventHandler({
        "IdentityRegister": RegisterEndpoint(),
    }, default_endpoint=AlwaysOkEndpoint())
