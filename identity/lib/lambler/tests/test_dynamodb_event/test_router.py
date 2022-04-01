from typing import Dict

from lambler.dynamodb_event.marker import EventBody
from lambler.dynamodb_event.router import DynamodbEventRouter, DynamodbEventHandler
from lambler.dynamodb_event.view import DynamodbStreamView
from .event_factory import simple_insert_event


def test_should_match_dynamodb_event():
    router = DynamodbEventRouter(stream_view_type=DynamodbStreamView.NEW_IMAGE)

    @router.insert()
    def on_insert(data: Dict = EventBody()):
        pass

    assert isinstance(router.match(simple_insert_event(), ...), DynamodbEventHandler)
