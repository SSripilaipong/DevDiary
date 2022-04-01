from http import HTTPStatus

from lambler import Lambler
from lambler.api_gateway.aws.version import AWSEventVersion
from lambler.api_gateway.endpoint.marker import JSONBody
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
