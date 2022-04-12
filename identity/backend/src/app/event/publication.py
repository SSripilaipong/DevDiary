from chamber.message.bus import MessageBus


def whitelist_messages(message_bus: MessageBus):
    message_bus.allow_publish_message("Identity-RegistrationEmailNeededToBeConfirmedEvent")
    message_bus.allow_publish_message("Identity-RegistrationConfirmedEvent")
    message_bus.allow_publish_message("Identity-UserCreatedEvent")
