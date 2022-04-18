from lambler.sns.message.processor import SNSMessageProcessor
from tests.test_sns_message.event_factory import simple_notification_event


def test_should_call_function():
    processor = SNSMessageProcessor()

    @processor.message("my-topic")
    def on_message():
        on_message.is_called = True

    processor.match(simple_notification_event("my-topic"), ...).handle()
    assert getattr(on_message, "is_called", False)
