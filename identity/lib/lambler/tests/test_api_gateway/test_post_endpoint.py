from pydantic import BaseModel
from typing import Dict, Type, Callable, Any

from chamber.data.field import Field
from chamber.data.model import DataModel
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


def test_should_pass_chamber_DataModel():
    class MyModel(DataModel):
        my_name: str = Field(getter=True)
        my_number: int = Field(getter=True)

    _test_passing_json_body(MyModel, lambda body, name: getattr(body, name))


def test_should_respond_422_when_request_JSONBody_without_content_type_json():
    _test_invalid_parameter(dict, {"data": "Hello World"}, headers={})


def test_should_respond_422_when_request_JSONBody_failed_to_convert_to_json():
    _test_invalid_parameter(dict, "abc123")


def test_should_respond_422_when_request_JSONBody_is_not_dict():
    _test_invalid_parameter(dict, '"Hello!"')


def test_should_respond_422_when_request_JSONBody_not_fit_to_model():
    class MyModel(BaseModel):
        my_name: str
        my_number: int

    _test_invalid_parameter(MyModel, {"Copy": "Paste", "Hello": "Engineer"})


def test_should_respond_422_when_request_JSONBody_not_fit_to_data_model():
    class MyModel(DataModel):
        my_name: str = Field(getter=True)
        my_number: int = Field(getter=True)

    _test_invalid_parameter(MyModel, {"Copy": "Paste", "Hello": "Engineer"})


def _test_invalid_parameter(model: Type, data: Any, headers=None):
    if headers is None:
        headers = {"content-type": "application/json"}

    router = APIGatewayRouter()

    @router.post("/do/something")
    def do_something(input_data: model = JSONBody()):
        pass

    event = simple_post_event("/do/something", data, headers=headers)
    assert router.match(event, ...).handle().status_code == 422


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


def test_should_return_value_from_function():
    router = APIGatewayRouter()

    @router.post("/hello")
    def hello():
        return "OK!"

    assert router.match(simple_post_event("/hello"), ...).handle().body == "OK!"
