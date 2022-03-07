from chamber.message.bus import MessageBus
from app.event.handler import handle_email_needed_confirmation, handle_registration_confirmed
from domain.identity.registration.event.confirmation_needed import RegistrationEmailNeededToBeConfirmedEvent
from domain.identity.registration.event.confirmed import RegistrationConfirmedEvent


def subscribe_for_messages(message_bus: MessageBus):
    # message_bus.subscribe(RegistrationEmailNeededToBeConfirmedEvent, handle_email_needed_confirmation)
    # message_bus.subscribe(RegistrationConfirmedEvent, handle_registration_confirmed)
    pass
