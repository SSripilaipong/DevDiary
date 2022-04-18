from lambler.base.function.input import FunctionInputSource
from lambler.sns.message.event import SNSMessageEvent


class MessageBodyInputSource(FunctionInputSource):
    def __init__(self, message: str):
        self._message = message

    @classmethod
    def from_event(cls, event: SNSMessageEvent) -> 'MessageBodyInputSource':
        assert len(event.records) == 1
        return cls(event.records[0].sns.message)

    def to_str(self) -> str:
        return self._message
