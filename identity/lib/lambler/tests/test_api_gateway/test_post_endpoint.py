from pytest import raises

from lambler.api_gateway.endpoint.exception import InvalidParameterError
from lambler.api_gateway.endpoint.marker import JSONBody
from lambler.api_gateway.router import APIGatewayRouter
from .event_factory import simple_post_event


def test_should_pass_json_body_as_dict():
    router = APIGatewayRouter()

    @router.post("/do/something")
    def do_something(my_body: dict = JSONBody()):
        do_something.data = my_body["data"]

    event = simple_post_event("/do/something", {"data": "Hello World"}, headers={"content-type": "application/json"})
    router.match(event, ...).handle()
    assert getattr(do_something, "data", "") == "Hello World"


def test_should_raise_InvalidParameterError_when_request_without_content_type_json():
    router = APIGatewayRouter()

    @router.post("/do/something")
    def do_something(my_body: dict = JSONBody()):
        pass

    event = simple_post_event("/do/something", {"data": "Hello World"})
    with raises(InvalidParameterError):
        router.match(event, ...).handle()
