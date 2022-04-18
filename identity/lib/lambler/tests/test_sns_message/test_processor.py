from pytest import raises
from pydantic import BaseModel
from typing import Dict, Type, TypeVar

from chamber.data.field import Field
from chamber.data.model import DataModel
from lambler.base.data.parser.exception import DataParsingError
from lambler.sns.message.marker import MessageBody
from lambler.sns.message.processor import SNSMessageProcessor
from tests.test_sns_message.event_factory import simple_notification_event


def test_should_call_function():
    processor = SNSMessageProcessor()

    @processor.message("my-topic")
    def on_message():
        on_message.is_called = True

    processor.match(simple_notification_event("my-topic"), ...).handle()
    assert getattr(on_message, "is_called", False)


def test_should_not_call_function_when_topic_not_matched():
    processor = SNSMessageProcessor()

    @processor.message("my-topic")
    def on_message():
        on_message.is_called = True

    processor.match(simple_notification_event("not-my-topic"), ...).handle()
    assert not getattr(on_message, "is_called", False)


def test_should_pass_payload_as_str():
    assert _get_passed_payload("Hello World", str) == "Hello World"


def test_should_pass_payload_as_Dict():
    assert _get_passed_payload('{"data": "abc", "num": 1234}', Dict) == {"data": "abc", "num": 1234}


def test_should_pass_payload_as_dict():
    assert _get_passed_payload('{"data": "abc", "num": 1234}', dict) == {"data": "abc", "num": 1234}


def test_should_raise_DataParsingError_when_cannot_parse_to_Dict():
    _test_raise_DataParsingError('Cannot Parse', Dict)


def test_should_raise_DataParsingError_when_cannot_parse_to_dict():
    _test_raise_DataParsingError('Cannot Parse', dict)


def test_should_pass_payload_as_pydantic_model():
    class MyModel(BaseModel):
        data: str
        num: int

    assert _get_passed_payload('{"data": "abc", "num": 1234}', MyModel) == MyModel(data="abc", num=1234)


def test_should_raise_DataParsingError_when_having_non_json_value_for_pydantic_model():
    class MyModel(BaseModel):
        data: str
        num: int

    _test_raise_DataParsingError('Cannot Parse', MyModel)


def test_should_raise_DataParsingError_when_having_invalid_structure_for_pydantic_model():
    class MyModel(BaseModel):
        data: str
        num: int

    _test_raise_DataParsingError('{"Copy": "Paste", "data": "Something"}', MyModel)


def test_should_pass_payload_as_chamber_data_model():
    class MyModel(DataModel):
        data: str = Field(getter=True)
        num: int = Field(getter=True)

    payload = _get_passed_payload('{"data": "abc", "num": 1234}', MyModel)
    assert payload.data == "abc" and payload.num == 1234


def test_should_raise_DataParsingError_when_having_non_json_value_for_chamber_model():
    class MyModel(DataModel):
        data: str = Field()
        num: int = Field()

    _test_raise_DataParsingError('Cannot Parse', MyModel)


def _test_raise_DataParsingError(message: str, type_: Type):
    processor = SNSMessageProcessor()

    @processor.message("my-topic")
    def on_message(payload_: type_ = MessageBody()):
        on_message.payload = payload_

    with raises(DataParsingError):
        processor.match(simple_notification_event("my-topic", message=message), ...).handle()


T = TypeVar("T")


def _get_passed_payload(message: str, type_: Type[T]) -> T:
    processor = SNSMessageProcessor()

    @processor.message("my-topic")
    def on_message(payload_: type_ = MessageBody()):
        on_message.payload = payload_

    processor.match(simple_notification_event("my-topic", message=message), ...).handle()
    return getattr(on_message, "payload", None)
