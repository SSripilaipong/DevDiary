from chamber.message.bus import MessageBus
from app.event.handler import handle_email_needed_confirmation, handle_registration_confirmed


def subscribe_for_messages(message_bus: MessageBus):
    message_bus.subscribe("Identity-RegistrationEmailNeededToBeConfirmedEvent", handle_email_needed_confirmation)
    message_bus.subscribe("Identity-RegistrationConfirmedEvent", handle_registration_confirmed)
