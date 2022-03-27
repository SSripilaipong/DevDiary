from pydantic import BaseModel
from typing import Dict

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


def test_should_pass_json_body_as_Dict():
    router = APIGatewayRouter()

    @router.post("/do/something")
    def do_something(my_body: Dict = JSONBody()):
        do_something.data = my_body["data"]

    event = simple_post_event("/do/something", {"data": "Hello World"}, headers={"content-type": "application/json"})
    router.match(event, ...).handle()
    assert getattr(do_something, "data", "") == "Hello World"


def test_should_raise_InvalidParameterError_when_request_JSONBody_without_content_type_json():
    router = APIGatewayRouter()

    @router.post("/do/something")
    def do_something(my_body: dict = JSONBody()):
        pass

    event = simple_post_event("/do/something", {"data": "Hello World"})
    with raises(InvalidParameterError):
        router.match(event, ...).handle()


def test_should_pass_pydantic_BaseModel():
    router = APIGatewayRouter()

    class MyModel(BaseModel):
        my_name: str
        my_number: int

    @router.post("/do/something")
    def do_something(input_data: MyModel = JSONBody()):
        do_something.data = {"my_name": input_data.my_name, "my_number": input_data.my_number}

    event = simple_post_event("/do/something", {"my_name": "Hello", "my_number": 123},
                              headers={"content-type": "application/json"})
    router.match(event, ...).handle()
    assert getattr(do_something, "data", "") == {"my_name": "Hello", "my_number": 123}


def test_should_raise_InvalidParameterError_when_request_JSONBody_failed_to_convert_to_json():
    router = APIGatewayRouter()

    @router.post("/do/something")
    def do_something(my_body: dict = JSONBody()):
        pass

    event = simple_post_event("/do/something", body="abc123", headers={"content-type": "application/json"})
    with raises(InvalidParameterError):
        router.match(event, ...).handle()


def test_should_raise_InvalidParameterError_when_request_JSONBody_is_not_dict():
    router = APIGatewayRouter()

    @router.post("/do/something")
    def do_something(my_body: dict = JSONBody()):
        pass

    event = simple_post_event("/do/something", body='"Hello!"', headers={"content-type": "application/json"})
    with raises(InvalidParameterError):
        router.match(event, ...).handle()
