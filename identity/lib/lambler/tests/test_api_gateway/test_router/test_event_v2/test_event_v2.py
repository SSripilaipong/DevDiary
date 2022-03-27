from typing import Dict

import json
import os.path

from pytest import fixture

from lambler.api_gateway.router import APIGatewayRouter, APIGatewayEventHandler


@fixture
def event() -> Dict:
    with open(os.path.join(os.path.dirname(__file__), "event-v2.json")) as file:
        return json.load(file)


def test_should_match_api_gateway_event(event: Dict):
    router = APIGatewayRouter()
    assert isinstance(router.match(event, ...), APIGatewayEventHandler)


def test_should_return_None_for_random_event():
    assert APIGatewayRouter().match({"Hello": "World"}, ...) is None
