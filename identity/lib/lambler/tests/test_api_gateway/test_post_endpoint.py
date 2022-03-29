from pydantic import BaseModel
from typing import Dict, Type, Callable

from pytest import raises

from lambler.api_gateway.endpoint.exception import InvalidParameterError
from lambler.api_gateway.endpoint.marker import JSONBody
from lambler.api_gateway.router import APIGatewayRouter
from .event_factory import simple_post_event


def test_should_pass_json_body_as_dict():
    _test_passing_json_body(dict, lambda body, name: body[name])


def test_should_pass_json_body_as_Dict():
    _test_passing_json_body(Dict, lambda body, name: body[name])


def test_should_pass_pydantic_BaseModel():
    class MyModel(BaseModel):
        my_name: str
        my_number: int

    _test_passing_json_body(MyModel, lambda body, name: getattr(body, name))


def test_should_raise_InvalidParameterError_when_request_JSONBody_without_content_type_json():
    router = APIGatewayRouter()

    @router.post("/do/something")
    def do_something(my_body: dict = JSONBody()):
        pass

    event = simple_post_event("/do/something", {"data": "Hello World"})
    with raises(InvalidParameterError):
        router.match(event, ...).handle()


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


def test_should_raise_InvalidParameterError_when_request_JSONBody_not_fit_to_model():
    router = APIGatewayRouter()

    class MyModel(BaseModel):
        my_name: str
        my_number: int

    @router.post("/do/something")
    def do_something(input_data: MyModel = JSONBody()):
        pass

    event = simple_post_event("/do/something", {"Copy": "Paste", "Hello": "Engineer"},
                              headers={"content-type": "application/json"})
    with raises(InvalidParameterError):
        router.match(event, ...).handle()


def _test_passing_json_body(model: Type, get_attr: Callable):
    router = APIGatewayRouter()

    @router.post("/do/something")
    def do_something(input_data: model = JSONBody()):
        do_something.data = {"my_name": get_attr(input_data, "my_name"),
                             "my_number": get_attr(input_data, "my_number")}

    event = simple_post_event("/do/something", {"my_name": "Hello", "my_number": 123},
                              headers={"content-type": "application/json"})
    router.match(event, ...).handle()
    assert getattr(do_something, "data", "") == {"my_name": "Hello", "my_number": 123}
