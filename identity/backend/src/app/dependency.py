import os

from app.event.publication import whitelist_messages
from app.event.subscription import subscribe_for_messages
from chamber.message.bus import MessageBus
from domain.registry import Registry
from emailling.in_memory import EmailServiceInMemory
from lambler.sns import SNSMessageBus
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
    table_name = os.environ["DB_TABLE_NAME"]

    import boto3
    dynamodb_client = boto3.client("dynamodb")

    bus = SNSMessageBus(boto3.client("sns"), os.environ["AWS_ACCOUNT_ID"], os.environ["AWS_REGION"],
                        prefix=f'{os.environ["ENVIRONMENT"]}-')
    _setup_message_bus(bus)

    registry = Registry()
    registry.all_registrations = AllRegistrationsInDynamodb(dynamodb_client, table_name=table_name)
    registry.all_users = AllUsersInMemory(topic_prefix="Identity-")
    registry.message_bus = bus
    registry.secret_manager = RandomSecretManager()
    registry.email_service = EmailServiceInMemory()


def _inject_test():
    bus = SynchronousMessageBus()
    _setup_message_bus(bus)

    registry = Registry()
    registry.all_registrations = AllRegistrationsInMemory(topic_prefix="Identity-")
    registry.all_users = AllUsersInMemory(topic_prefix="Identity-")
    registry.message_bus = bus
    registry.secret_manager = RandomSecretManager()
    registry.email_service = EmailServiceInMemory()


def _setup_message_bus(bus: MessageBus):
    subscribe_for_messages(bus)
    whitelist_messages(bus)
