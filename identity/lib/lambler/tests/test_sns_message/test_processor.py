from typing import Dict

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
    processor = SNSMessageProcessor()

    @processor.message("my-topic")
    def on_message(payload: str = MessageBody()):
        on_message.payload = payload

    processor.match(simple_notification_event("my-topic", message="Hello World"), ...).handle()
    assert getattr(on_message, "payload", None) == "Hello World"
