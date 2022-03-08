from app.event.publication import whitelist_messages
from app.event.subscription import subscribe_for_messages
from domain.registry import Registry
from in_memory_email_service import EmailServiceInMemory
from in_memory_persistence.identity.registration.repository import AllRegistrationsInMemory
from in_memory_persistence.identity.user.repository import AllUsersInMemory
from random_secret_manager import RandomSecretManager
from chamber.message.bus.synchronous import SynchronousMessageBus


def inject():
    registry = Registry()
    registry.all_registrations = AllRegistrationsInMemory()
    registry.all_users = AllUsersInMemory()
    registry.message_bus = _get_message_bus()
    registry.secret_manager = RandomSecretManager()
    registry.email_service = EmailServiceInMemory()


def _get_message_bus() -> SynchronousMessageBus:
    message_bus = SynchronousMessageBus()
    subscribe_for_messages(message_bus)
    whitelist_messages(message_bus)
    return message_bus
