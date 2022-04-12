from typing import Type, Callable, Any

import app.main
from chamber.message import Message
from chamber.message.bus import MessageBus
from chamber.message.bus.bus import M
from domain.identity.registration.event.confirmation_needed import RegistrationEmailNeededToBeConfirmedEvent
from domain.registry import Registry
from lambler.dynamodb_event.data.view import DynamodbStreamView
from lambler.testing.dynamodb_event.simulator import DynamodbEventSimulator


class MessageBusMock(MessageBus):
    def __init__(self):
        self.published_message = None

    def publish(self, message: Message):
        self.published_message = message

    def subscribe(self, message: Type[M], handler: Callable[[M], Any]):
        pass

    def allow_publish_message(self, message: Type[Message]):
        pass


def test_should_publish_RegistrationEmailNeededToBeConfirmedEvent():
    Registry().message_bus = bus = MessageBusMock()

    simulator = DynamodbEventSimulator(app.main.handler, DynamodbStreamView.NEW_IMAGE)
    response = simulator.insert({
        "_Partition": "registration#test@devdiary.link",
        "_SortKey": "registration#test@devdiary.link",
        "_LatestEvents": [
            {
                "name": "RegistrationEmailNeededToBeConfirmedEvent",
                "body": {
                    "confirmationCode": "0864e05e-3b20-4341-b822-1de8f3b0b8d4",
                    "email": "test@devdiary.link",
                },
            },
        ],
    }, "_Partition", "_SortKey")
    assert response.all_success()

    message = bus.published_message
    assert isinstance(message, RegistrationEmailNeededToBeConfirmedEvent)
    assert message.email.str() == "test@devdiary.link"
    assert message.confirmation_code == "0864e05e-3b20-4341-b822-1de8f3b0b8d4"
