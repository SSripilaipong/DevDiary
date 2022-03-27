import json
import os.path

from pytest import fixture
from typing import Dict

from lambler.api_gateway.aws.event_v2 import AWSAPIGatewayEventV2
from lambler.api_gateway.event import APIGatewayEvent


@fixture
def event_v2() -> Dict:
    with open(os.path.join(os.path.dirname(__file__), "event-v2.json")) as file:
        return json.load(file)


def test_should_normalize_to_APIGatewayEvent(event_v2: Dict):
    expected = APIGatewayEvent(path="/default/something", method="GET", query_string_parameters={}, body="",
                               headers={
                                   "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp",
                                   "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ...",
                               })
    assert AWSAPIGatewayEventV2(**event_v2).normalize() == expected
