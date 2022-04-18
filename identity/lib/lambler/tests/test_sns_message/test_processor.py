from pytest import raises
from pydantic import BaseModel
from typing import Dict, Type, Any

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
    _test_passed_payload("Hello World", str, "Hello World")


def test_should_pass_payload_as_Dict():
    _test_passed_payload('{"data": "abc", "num": 1234}', Dict, {"data": "abc", "num": 1234})


def test_should_pass_payload_as_dict():
    _test_passed_payload('{"data": "abc", "num": 1234}', dict, {"data": "abc", "num": 1234})


def test_should_raise_DataParsingError_when_cannot_parse_to_Dict():
    _test_raise_DataParsingError('Cannot Parse', Dict)


def test_should_raise_DataParsingError_when_cannot_parse_to_dict():
    _test_raise_DataParsingError('Cannot Parse', dict)


def test_should_pass_payload_as_pydantic_model():
    class MyModel(BaseModel):
        data: str
        num: int

    _test_passed_payload('{"data": "abc", "num": 1234}', MyModel, MyModel(data="abc", num=1234))


def _test_raise_DataParsingError(message: str, type_: Type):
    processor = SNSMessageProcessor()

    @processor.message("my-topic")
    def on_message(payload_: type_ = MessageBody()):
        on_message.payload = payload_

    with raises(DataParsingError):
        processor.match(simple_notification_event("my-topic", message=message), ...).handle()


def _test_passed_payload(message: str, type_: Type, expected_payload: Any):
    processor = SNSMessageProcessor()

    @processor.message("my-topic")
    def on_message(payload_: type_ = MessageBody()):
        on_message.payload = payload_

    processor.match(simple_notification_event("my-topic", message=message), ...).handle()
    assert getattr(on_message, "payload", None) == expected_payload
