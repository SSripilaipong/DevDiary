from pytest import raises

from domain.identity.registration.exception import EmailAlreadyRegisteredException
from domain.identity.registration.registration import Registration
from domain.identity.registration.repository import AllRegistrations
from domain.identity.usecase.registration import register_user
from domain.identity.user.exception import UsernameAlreadyRegisteredException
from domain.identity.value_object.email import Email
from domain.identity.value_object.password import Password
from domain.identity.value_object.username import Username
from domain.registry import Registry


def test_should_create_registration():
    all_registrations = get_all_registrations()
    Registry().all_registrations = all_registrations
    register_user(Username.as_is("username"), Password.as_is("password"), "display_name", Email.as_is("email"))

    registration = all_registrations.created_registration
    assert registration.username.str() == "username" \
           and registration.display_name == "display_name" \
           and registration.email.str() == "email"


def test_should_generate_confirmation_code():
    all_registrations = get_all_registrations()
    Registry().all_registrations = all_registrations
    register_user(Username.as_is(""), Password.as_is(""), "", Email.as_is(""))
    assert all_registrations.confirmation_code_generated


def test_should_not_allow_duplicate_username():
    Registry().all_registrations = get_all_registrations(create_exception=UsernameAlreadyRegisteredException())
    with raises(UsernameAlreadyRegisteredException):
        register_user(Username.as_is(""), Password.as_is(""), "", Email.as_is(""))


def test_should_not_allow_duplicate_email():
    Registry().all_registrations = get_all_registrations(create_exception=EmailAlreadyRegisteredException())
    with raises(EmailAlreadyRegisteredException):
        register_user(Username.as_is(""), Password.as_is(""), "", Email.as_is(""))


def get_all_registrations(*, create_exception=None) -> 'AllRegistrationsDummy':
    return AllRegistrationsDummy(create_exception=create_exception)


class AllRegistrationsDummy(AllRegistrations):
    def __init__(self, create_exception=None):
        self._create_exception = create_exception

        self.created_registration = None
        self.confirmation_code_generated = False

    def generate_confirmation_code(self) -> str:
        self.confirmation_code_generated = True

    def create(self, registration: Registration) -> Registration:
        if self._create_exception:
            raise self._create_exception
        self.created_registration = registration

    def from_email(self, email: Email) -> Registration:
        pass

    def save(self, registration: Registration):
        pass

