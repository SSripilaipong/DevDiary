from lambler.sns.message.processor import SNSMessageProcessor


def test_should_call_function():
    processor = SNSMessageProcessor()

    @processor.message()
    def on_message():
        on_message.is_called = True

    processor.match({}, ...).handle()
    assert getattr(on_message, "is_called", False)
