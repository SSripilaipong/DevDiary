from typing import Dict, Type

from chamber.message import Message
from domain.identity.registration.event.confirmation_needed import RegistrationEmailNeededToBeConfirmedEvent
from domain.registry import Registry
from lambler.dynamodb_event import DynamodbEventProcessor
from lambler.dynamodb_event.data.view import DynamodbStreamView
from lambler.dynamodb_event.marker import EventBody

dynamodb_event = DynamodbEventProcessor(DynamodbStreamView.NEW_IMAGE)


@dynamodb_event.insert()
def on_insert(data: Dict = EventBody()):
    message_bus = Registry().message_bus
    events = data.get("_LatestEvents", [])
    for raw in events:
        event = _deserialize_message(raw)

        message_bus.publish(event)


def _get_message_type(name: str) -> Type[Message]:
    if name == "RegistrationEmailNeededToBeConfirmedEvent":
        return RegistrationEmailNeededToBeConfirmedEvent

    raise NotImplementedError()


def _deserialize_message(event: Dict) -> Message:
    name = event.get("name", None)
    type_ = _get_message_type(name)
    return type_.from_dict(event)
