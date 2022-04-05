from http import HTTPStatus

from typing import Dict

from lambler import Lambler
from lambler.api_gateway.aws.version import AWSEventVersion
from lambler.api_gateway.marker import JSONBody
from lambler.api_gateway.response import JSONResponse
from lambler.api_gateway.router import APIGatewayRouter
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


def test_should_make_post_request_with_json_body():
    router = APIGatewayRouter()

    @router.post("/hello")
    def hello(request: Dict = JSONBody()):
        return {"request": request}

    lambler = Lambler()
    lambler.include_pattern(router)

    requester = HTTPRequester(lambler)
    response = requester.post("/hello", body={"Hello": "World"})
    assert response.body_dict["request"] == {"Hello": "World"}


def test_should_return_from_raw_response():
    router = APIGatewayRouter()

    @router.get("/hello")
    def hello():
        return JSONResponse({"Hello": "World"}, HTTPStatus.CREATED)

    lambler = Lambler()
    lambler.include_pattern(router)

    requester = HTTPRequester(lambler)
    response = requester.get("/hello")
    assert response.status_code == HTTPStatus.CREATED
    assert response.body_dict == {"Hello": "World"}


def test_should_support_aws_api_event_v2():
    router = APIGatewayRouter(event_version=AWSEventVersion.V2)

    @router.get("/hello")
    def hello():
        return JSONResponse({"Hello": "World"}, HTTPStatus.CREATED)

    lambler = Lambler()
    lambler.include_pattern(router)

    requester = HTTPRequester(lambler, event_version=AWSEventVersion.V2)
    response = requester.get("/hello")
    assert response.status_code == HTTPStatus.CREATED
    assert response.body_dict == {"Hello": "World"}
