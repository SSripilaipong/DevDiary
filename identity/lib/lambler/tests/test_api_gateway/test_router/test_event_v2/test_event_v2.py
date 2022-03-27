from typing import Dict

import json
import os.path

from pytest import fixture

from lambler.api_gateway.router import APIGatewayRouter, APIGatewayEventHandler
from .event_factory import simple_post_event, simple_get_event


@fixture
def event() -> Dict:
    with open(os.path.join(os.path.dirname(__file__), "event-v2.json")) as file:
        return json.load(file)


def test_should_match_api_gateway_event(event: Dict):
    router = APIGatewayRouter()

    router.get("/default/something")(lambda: ...)

    assert isinstance(router.match(event, ...), APIGatewayEventHandler)


def test_should_return_None_for_random_event():
    assert APIGatewayRouter().match({"Hello": "World"}, ...) is None


def test_should_handle_event_with_get_method(event):
    router = APIGatewayRouter()

    @router.get("/default/something")
    def get_something():
        get_something.is_called = True

    router.match(event, ...).handle()
    assert getattr(get_something, "is_called", False)


def test_should_handle_event_with_post_method():
    router = APIGatewayRouter()

    @router.post("/default/something")
    def post_something():
        post_something.is_called = True

    router.match(simple_post_event("/default/something"), ...).handle()
    assert getattr(post_something, "is_called", False)


def test_should_select_endpoints_with_same_path_by_method():
    router = APIGatewayRouter()

    @router.post("/default/something")
    def post_something():
        post_something.is_called = True

    @router.get("/default/something")
    def get_something():
        get_something.is_called = True

    router.match(simple_post_event("/default/something"), ...).handle()
    assert getattr(post_something, "is_called", False) and not getattr(get_something, "is_called", False)
    post_something.is_called = False

    router.match(simple_get_event("/default/something"), ...).handle()
    assert not getattr(post_something, "is_called", False) and getattr(get_something, "is_called", False)
