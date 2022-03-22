import uuid
from typing import Dict, List, Set

from chamber.aggregate.version_increase import AggregateVersionIncrease
from chamber.message import Message
from chamber.repository import EntityOutdated
from domain.identity.registration.exception import (
    EmailAlreadyRegisteredException, RegistrationNotFoundException, )
from domain.identity.user.exception import UsernameAlreadyRegisteredException
from domain.identity.registration.registration import Registration
from domain.identity.registration.repository import AllRegistrations
from domain.identity.value_object.email import Email
from domain.identity.value_object.username import Username
from domain.registry import Registry


class AllRegistrationsInMemory(AllRegistrations):
    def __init__(self, registrations: Dict[Email, Registration] = None,
                 active_or_confirmed_usernames: Set[Username] = None):
        self._registrations = registrations or dict()
        self._active_or_confirmed_usernames = active_or_confirmed_usernames or set()

    def create(self, registration: Registration) -> Registration:
        """
        :raises:
            EmailAlreadyRegisteredException
            UsernameAlreadyRegisteredException
        """
        if registration.email in self._registrations:
            raise EmailAlreadyRegisteredException()
        if registration.username in self._active_or_confirmed_usernames:
            raise UsernameAlreadyRegisteredException()
        self._active_or_confirmed_usernames.add(registration.username)
        self._store_and_handle_outbox(registration)
        return registration

    def from_email(self, email: Email) -> Registration:
        """
        :raises:
            RegistrationNotFoundException
        """
        if email not in self._registrations:
            raise RegistrationNotFoundException()
        return self._registrations[email]

    def save(self, registration: Registration):
        """
        :raises:
            EntityOutdated
            RegistrationNotFoundException
        """
        matched = self._registrations.get(registration.email, None)
        if matched is None:
            raise RegistrationNotFoundException()
        if registration.aggregate_version < matched.aggregate_version:
            raise EntityOutdated()
        registration.increase_aggregate_version_by(AggregateVersionIncrease.create(1))
        self._store_and_handle_outbox(registration)

    def generate_confirmation_code(self) -> str:
        return str(uuid.uuid4())

    def _store_and_handle_outbox(self, registration: Registration):
        outbox = registration.get_aggregate_outbox_messages()
        registration.clear_aggregate_outbox_messages()
        self._registrations[registration.email] = registration
        self._handle_outbox(outbox)

    @staticmethod
    def _handle_outbox(outbox: List[Message]):
        message_bus = Registry().message_bus
        for message in outbox:
            message_bus.publish(message)
