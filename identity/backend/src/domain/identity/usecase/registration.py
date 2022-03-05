from typing import TYPE_CHECKING

from chamber.transaction import transaction
from domain.identity.security.password import hash_password
from domain.identity.registration.registration import Registration
from domain.identity.value_object.username import Username
from domain.registry import Registry


def register_user(username: str, password: str, display_name: str, email: str) -> Registration:
    """
    :raises:
        EmailAlreadyRegisteredException
        UsernameAlreadyRegisteredException
    """
    all_registrations = Registry().all_registrations
    confirmation_code = all_registrations.generate_confirmation_code()
    registration = Registration.create(Username(username), hash_password(password), display_name, email,
                                       confirmation_code)
    return all_registrations.create(registration)


@transaction
def confirm_registration(email: str, confirmation_code: str):
    """
    :raises:
        RegistrationNotFoundException
        RegistrationCanNotBeConfirmedTwiceException
        RegistrationConfirmationCodeNotMatchedException
    """
    all_registrations = Registry().all_registrations
    registration = all_registrations.from_email(email)
    registration.confirm(confirmation_code)
    all_registrations.save(registration)


def send_confirmation_email(email: str, confirmation_code: str):
    Registry().email_service.send_confirmation_email(email, confirmation_code)


if TYPE_CHECKING:
    def confirm_registration(email: str, confirmation_code: str): ...
