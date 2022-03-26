import os

from app.event.publication import whitelist_messages
from app.event.subscription import subscribe_for_messages
from domain.registry import Registry
from emailling.in_memory import EmailServiceInMemory
from persistence.dynamodb.identity.registration.repository import AllRegistrationsInDynamodb
from persistence.in_memory.identity.registration.repository import AllRegistrationsInMemory
from persistence.in_memory.identity.user.repository import AllUsersInMemory
from random_secret_manager import RandomSecretManager
from chamber.message.bus.synchronous import SynchronousMessageBus


def inject():
    if os.environ.get("ENVIRONMENT", None) == "prod":
        _inject_prod()
    else:
        _inject_test()


def _inject_prod():
    import boto3
    dynamodb_client = boto3.client("dynamodb")
    registry = Registry()
    registry.all_registrations = AllRegistrationsInDynamodb(dynamodb_client, table_name="Identity")
    registry.all_users = AllUsersInMemory()
    registry.message_bus = _get_message_bus()
    registry.secret_manager = RandomSecretManager()
    registry.email_service = EmailServiceInMemory()


def _inject_test():
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
