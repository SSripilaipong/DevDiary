from chamber.message.bus import MessageBus
from domain.identity.registration.event.confirmation_needed import RegistrationEmailNeededToBeConfirmedEvent
from domain.identity.registration.event.confirmed import RegistrationConfirmedEvent
from domain.identity.user.event.created import UserCreatedEvent


def whitelist_messages(message_bus: MessageBus):
    message_bus.allow_publish_message(RegistrationEmailNeededToBeConfirmedEvent)
    message_bus.allow_publish_message(RegistrationConfirmedEvent)
    message_bus.allow_publish_message(UserCreatedEvent)
