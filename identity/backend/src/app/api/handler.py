from api_gateway.handler import ApiGatewayServiceEventHandler
from app.api.endpoint.default import AlwaysOkEndpoint
from app.api.endpoint.register import RegisterEndpoint


def get_api_gateway_handler() -> ApiGatewayServiceEventHandler:
    return ApiGatewayServiceEventHandler({
        "IdentityRegister": RegisterEndpoint(),
    }, default_endpoint=AlwaysOkEndpoint())
