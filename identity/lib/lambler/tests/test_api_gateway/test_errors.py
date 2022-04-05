from http import HTTPStatus

from lambler import Lambler
from lambler.api_gateway.aws.version import AWSEventVersion
from lambler.api_gateway.marker import JSONBody
from lambler.api_gateway.router import APIGatewayRouter
from lambler.testing.api_gateway.requester import HTTPRequester


def test_should_response_unprocessable_entity_when_json_body_required_but_none_given():
    lambler = Lambler()
    router = APIGatewayRouter(event_version=AWSEventVersion.V2)

    @router.post("/")
    def post(data: dict = JSONBody()):
        return ""

    lambler.include_pattern(router)
    requester = HTTPRequester(lambler, event_version=AWSEventVersion.V2)
    response = requester.post("/")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_should_respond_internal_server_error_when_endpoint_raises_unexpected_exception():
    lambler = Lambler()
    router = APIGatewayRouter(event_version=AWSEventVersion.V2)

    @router.get("/")
    def get():
        raise ZeroDivisionError()

    lambler.include_pattern(router)
    requester = HTTPRequester(lambler, event_version=AWSEventVersion.V2)
    response = requester.get("/")
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
