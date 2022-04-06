from lambler.base.function.input import FunctionInputSourceCollection
from lambler.dynamodb_event.data.event import DynamodbEvent
from lambler.dynamodb_event.input.new_image import DynamodbEventNewImageInputSource


class DynamodbEventInputCollection(FunctionInputSourceCollection):
    @classmethod
    def from_event(cls, event: DynamodbEvent) -> 'DynamodbEventInputCollection':
        return cls({
            DynamodbEventNewImageInputSource: DynamodbEventNewImageInputSource.from_event(event),
        })

    @property
    def new_image(self):
        return self.of(DynamodbEventNewImageInputSource)
