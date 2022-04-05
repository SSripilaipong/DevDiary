from typing import Dict

from lambler.base.handler import Handler
from lambler.dynamodb_event.processor import DynamodbEventProcessor
from lambler.dynamodb_event.marker import EventBody
from lambler.dynamodb_event.model.view import DynamodbStreamView
from .event_factory import simple_insert_event


def test_should_match_dynamodb_event():
    processor = DynamodbEventProcessor(stream_view_type=DynamodbStreamView.NEW_IMAGE)

    @processor.insert()
    def on_insert(data: Dict = EventBody()):
        pass

    assert isinstance(processor.match(simple_insert_event(), ...), Handler)


def test_should_not_match_random_event():
    processor = DynamodbEventProcessor(stream_view_type=DynamodbStreamView.NEW_IMAGE)

    @processor.insert()
    def on_insert():
        pass

    assert processor.match({"Hello": "World"}, ...) is None


def test_should_not_match_when_operation_not_registered():
    processor = DynamodbEventProcessor(stream_view_type=DynamodbStreamView.NEW_IMAGE)

    assert processor.match(simple_insert_event(), ...) is None


def test_should_should_call_function():
    processor = DynamodbEventProcessor(stream_view_type=DynamodbStreamView.NEW_IMAGE)

    @processor.insert()
    def on_insert():
        on_insert.is_called = True

    processor.match(simple_insert_event(), ...).handle()
    assert getattr(on_insert, "is_called", False)


def test_should_pass_body_to_function():
    processor = DynamodbEventProcessor(stream_view_type=DynamodbStreamView.NEW_IMAGE)

    @processor.insert()
    def on_insert(body: Dict = EventBody()):
        on_insert.read_data = body

    raw_body = {
        "name": {"S": "CPEngineer"},
        "email": {"S": "cpeng@devdiary.link"},
        "age": {"N": "11"},
    }
    processor.match(simple_insert_event(body=raw_body), ...).handle()
    assert getattr(on_insert, "read_data", None) == {"name": "CPEngineer", "email": "cpeng@devdiary.link", "age": 11}
