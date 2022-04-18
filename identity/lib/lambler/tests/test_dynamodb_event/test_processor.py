from operator import getitem

from decimal import Decimal

from pydantic import BaseModel
from typing import Dict, Type, Callable

from chamber.data.field import Field
from chamber.data.model import DataModel
from lambler.base.handler import Handler
from lambler.base.response import LamblerResponse
from lambler.dynamodb_event.processor import DynamodbEventProcessor
from lambler.dynamodb_event.marker import EventBody
from lambler.dynamodb_event.data.view import DynamodbStreamView
from .event_factory import simple_insert_event, simple_insert_event_multiple_records, simple_remove_event


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
    _test_support_model_body(Dict, getitem)


def test_should_support_passing_pydantic_body_to_function():
    class MyData(BaseModel):
        name: str
        email: str
        age: int

    _test_support_model_body(MyData, getattr)


def test_should_support_passing_chamber_body_to_function():
    class MyData(DataModel):
        name: str = Field(getter=True)
        email: str = Field(getter=True)
        age: Decimal = Field(getter=True)

    _test_support_model_body(MyData, getattr)


def test_should_return_LamblerResponse():
    processor = DynamodbEventProcessor(stream_view_type=DynamodbStreamView.NEW_IMAGE)

    @processor.insert()
    def on_insert():
        pass

    assert isinstance(processor.match(simple_insert_event(), ...).handle(), LamblerResponse)


def test_should_not_report_item_failure_when_success():
    processor = DynamodbEventProcessor(stream_view_type=DynamodbStreamView.NEW_IMAGE)

    @processor.insert()
    def on_insert():
        pass

    response = processor.match(simple_insert_event(event_id="123"), ...).handle().to_dict()
    assert "batchItemFailures" in response
    assert len(response["batchItemFailures"]) == 0


def test_should_report_item_failure_when_error_raised():
    processor = DynamodbEventProcessor(stream_view_type=DynamodbStreamView.NEW_IMAGE)

    @processor.insert()
    def on_insert():
        raise Exception()

    response = processor.match(simple_insert_event(event_id="123"), ...).handle().to_dict()
    assert len(response["batchItemFailures"]) == 1
    assert response["batchItemFailures"][0]["itemIdentifier"] == "123"


def test_should_support_multiple_records():
    processor = DynamodbEventProcessor(stream_view_type=DynamodbStreamView.NEW_IMAGE)

    inputs = []

    @processor.insert()
    def on_insert(data: Dict = EventBody()):
        inputs.append(data["num"])

    processor.match(simple_insert_event_multiple_records(nums=[1, 2]), ...).handle()
    assert inputs == [1, 2]


def test_should_report_only_failed_items_when_multiple_records_passed():
    processor = DynamodbEventProcessor(stream_view_type=DynamodbStreamView.NEW_IMAGE)

    @processor.insert()
    def on_insert(data: Dict = EventBody()):
        if data["num"] in (2, 3):
            raise Exception()

    records = simple_insert_event_multiple_records(nums=[1, 2, 3, 4], event_ids=["e1", "e2", "e3", "e4"])
    response = processor.match(records, ...).handle().to_dict()
    assert len(response["batchItemFailures"]) == 2
    assert {report["itemIdentifier"] for report in response["batchItemFailures"]} == {"e2", "e3"}


def test_should_report_item_failure_when_data_passing_failed():
    processor = DynamodbEventProcessor(stream_view_type=DynamodbStreamView.NEW_IMAGE)

    class MyModel(BaseModel):
        num: int

    @processor.insert()
    def on_insert(data: MyModel = EventBody()):
        pass

    response = processor.match(simple_insert_event(body={"Hello": "World"}, event_id="e1"), ...).handle().to_dict()
    assert response["batchItemFailures"][0]["itemIdentifier"] == "e1"


def test_should_deny_different_types_of_event():
    processor = DynamodbEventProcessor(stream_view_type=DynamodbStreamView.NEW_IMAGE)

    @processor.insert()
    def on_insert():
        on_insert.is_called = True

    processor.match(simple_remove_event(), ...).handle()
    assert not getattr(on_insert, "is_called", False)


def _test_support_model_body(model: Type, get_attr: Callable):
    processor = DynamodbEventProcessor(stream_view_type=DynamodbStreamView.NEW_IMAGE)

    @processor.insert()
    def on_insert(body: model = EventBody()):
        on_insert.read_data = body

    raw_body = {
        "name": {"S": "CPEngineer"},
        "email": {"S": "cpeng@devdiary.link"},
        "age": {"N": "11"},
    }
    processor.match(simple_insert_event(body=raw_body), ...).handle()
    read_data = getattr(on_insert, "read_data", None)
    assert read_data is not None
    assert get_attr(read_data, "name") == "CPEngineer"
    assert get_attr(read_data, "email") == "cpeng@devdiary.link"
    assert get_attr(read_data, "age") == 11
