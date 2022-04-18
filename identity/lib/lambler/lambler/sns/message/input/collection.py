from lambler.base.function.input import FunctionInputSourceCollection
from lambler.sns.message.event import SNSMessageEvent
from lambler.sns.message.input.body import MessageBodyInputSource


class SNSMessageInputCollection(FunctionInputSourceCollection):
    @classmethod
    def from_event(cls, event: SNSMessageEvent) -> 'SNSMessageInputCollection':
        return cls({
            MessageBodyInputSource: MessageBodyInputSource.from_event(event),
        })

    @property
    def body(self) -> MessageBodyInputSource:
        return self.of(MessageBodyInputSource)
