from lambler import Lambler
from lambler.api_gateway.router import APIGatewayRouter
from lambler.api_gateway.status import HTTPStatus
from lambler.testing.api_gateway.requester import HTTPRequester


def test_should_make_get_request():
    router = APIGatewayRouter()

    @router.get("/hello")
    def hello():
        return {"message": "OK!"}

    lambler = Lambler()
    lambler.include_pattern(router)

    requester = HTTPRequester(lambler)
    response = requester.get("/hello")
    assert response.status_code == HTTPStatus.OK
    assert response.body_dict == {"message": "OK!"}


def test_should_make_post_request():
    router = APIGatewayRouter()

    @router.post("/hello")
    def hello():
        return {"message": "OK!"}

    lambler = Lambler()
    lambler.include_pattern(router)

    requester = HTTPRequester(lambler)
    response = requester.post("/hello")
    assert response.status_code == HTTPStatus.OK
    assert response.body_dict == {"message": "OK!"}
