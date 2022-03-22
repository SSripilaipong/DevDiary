from devdiary.specification.registration import RegistrationDriver

from domain.identity.usecase.registration import register_user, confirm_registration
from domain.identity.usecase.login import login_with_username_and_password
from domain.identity.usecase.user import get_username_from_user_token
from domain.identity.value_object.display_name import DisplayName
from domain.identity.value_object.email import Email
from domain.identity.value_object.password import Password
from domain.identity.value_object.username import Username
from domain.registry import Registry
from app.event.subscription import subscribe_for_messages
from app.event.publication import whitelist_messages
from emailling.in_memory import EmailServiceInMemory
from persistence.in_memory.identity.registration.repository import AllRegistrationsInMemory
from persistence.in_memory.identity.user.repository import AllUsersInMemory
from random_secret_manager import RandomSecretManager
from chamber.message.bus.synchronous import SynchronousMessageBus


class DomainRegistrationDriver(RegistrationDriver):
    def __init__(self, user_token: str = None):
        self._user_token = user_token
        self._email_service = EmailServiceInMemory()

        registry = Registry()
        registry.all_registrations = AllRegistrationsInMemory()
        registry.all_users = AllUsersInMemory()
        registry.message_bus = _get_message_bus()
        registry.secret_manager = RandomSecretManager()
        registry.email_service = self._email_service

    def submit_registration(self, username: str, password: str, display_name: str, email: str):
        """
        :raises:
            InvalidUsernameException
            InvalidPasswordException
            InvalidEmailException
            InvalidDisplayNameException
            EmailAlreadyRegisteredException
            UsernameAlreadyRegisteredException
        """
        register_user(Username(username), Password(password), DisplayName(display_name), Email(email))

    def get_confirmation_code_from_email(self, email: str) -> str:
        """
        :raises:
            ConfirmationEmailNotFoundException
        """
        return self._email_service.get_latest_confirmation_code(Email.as_is(email))

    def confirm_registration_by_email(self, email: str, confirmation_code: str):
        confirm_registration(Email.as_is(email), confirmation_code)

    def login_with_username_and_password(self, username: str, password: str):
        self._user_token = login_with_username_and_password(Username.as_is(username), Password.as_is(password))

    def get_current_username(self) -> str:
        return get_username_from_user_token(self._user_token).str()


def _get_message_bus() -> SynchronousMessageBus:
    message_bus = SynchronousMessageBus()
    subscribe_for_messages(message_bus)
    whitelist_messages(message_bus)
    return message_bus
