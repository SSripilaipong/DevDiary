import json

import os

from typing import Dict

from pytest import fixture

from lambler.api_gateway.router import APIGatewayRouter


@fixture
def event_v2() -> Dict:
    with open(os.path.join(os.path.dirname(__file__), "event-v2.json")) as file:
        return json.load(file)


def test_should_read_event_v2_when_specify_event_version_in_router(event_v2: Dict):
    router = APIGatewayRouter(event_version="v2")

    @router.get("/default/something")
    def get_something():
        get_something.is_called = True

    router.match(event_v2, ...).handle()
    assert getattr(get_something, "is_called", False)
