from typing import Dict

from lambler.base.handler import Handler
from lambler.dynamodb_event.processor import DynamodbEventProcessor
from lambler.dynamodb_event.marker import EventBody
from lambler.dynamodb_event.view import DynamodbStreamView
from .event_factory import simple_insert_event


def test_should_match_dynamodb_event():
    router = DynamodbEventProcessor(stream_view_type=DynamodbStreamView.NEW_IMAGE)

    @router.insert()
    def on_insert(data: Dict = EventBody()):
        pass

    assert isinstance(router.match(simple_insert_event(), ...), Handler)


def test_should_not_match_random_event():
    router = DynamodbEventProcessor(stream_view_type=DynamodbStreamView.NEW_IMAGE)

    @router.insert()
    def on_insert():
        pass

    assert router.match({"Hello": "World"}, ...) is None


def test_should_not_match_when_operation_not_registered():
    processor = DynamodbEventProcessor(stream_view_type=DynamodbStreamView.NEW_IMAGE)

    assert processor.match(simple_insert_event(), ...) is None
