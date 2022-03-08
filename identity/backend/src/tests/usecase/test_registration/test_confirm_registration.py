from pytest import raises

from domain.identity.registration.exception import RegistrationNotFoundException, \
    RegistrationCanNotBeConfirmedTwiceException, RegistrationConfirmationCodeNotMatchedException
from domain.identity.registration.registration import Registration
from domain.identity.registration.repository import AllRegistrations
from domain.identity.usecase.registration import confirm_registration
from domain.identity.value_object.email import Email
from domain.identity.value_object.username import Username
from domain.registry import Registry


def test_should_confirm_registration():
    registration = Registration.create(Username.as_is(""), b"", "", Email.as_is("aaa@amail.com"), "CONFIRM!!!")
    Registry().all_registrations = AllRegistrationsDummy(from_email_return=registration)
    confirm_registration(Email.as_is("aaa@amail.com"), "CONFIRM!!!")
    assert registration.is_confirmed()


def test_should_save_registration():
    registration = Registration.create(Username.as_is(""), b"", "", Email.as_is("aaa@amail.com"), "CONFIRM!!!")
    Registry().all_registrations = all_registrations = AllRegistrationsDummy(from_email_return=registration)
    confirm_registration(Email.as_is("aaa@amail.com"), "CONFIRM!!!")

    saved_registration = all_registrations.saved_registration
    assert registration == saved_registration


def test_should_raise_RegistrationNotFoundException():
    Registry().all_registrations = AllRegistrationsDummy(from_email_exception=RegistrationNotFoundException())
    with raises(RegistrationNotFoundException):
        confirm_registration(Email.as_is(""), "")


def test_should_raise_RegistrationCanNotBeConfirmedTwiceException():
    registration = Registration.create(Username.as_is(""), b"", "", Email.as_is("aaa@amail.com"), "xxx")
    registration.confirm("xxx")

    Registry().all_registrations = AllRegistrationsDummy(from_email_return=registration)
    with raises(RegistrationCanNotBeConfirmedTwiceException):
        confirm_registration(Email.as_is("aaa@amail.com"), "")


def test_should_raise_RegistrationConfirmationCodeNotMatchedException():
    registration = Registration.create(Username.as_is(""), b"", "", Email.as_is("aaa@amail.com"), "AAA")
    Registry().all_registrations = AllRegistrationsDummy(from_email_return=registration)
    with raises(RegistrationConfirmationCodeNotMatchedException):
        confirm_registration(Email.as_is("aaa@amail.com"), "BBB")


class AllRegistrationsDummy(AllRegistrations):
    def __init__(self, from_email_return=None, from_email_exception=None):
        self._from_email_return = from_email_return
        self._from_email_exception = from_email_exception

        self.saved_registration = None

    def generate_confirmation_code(self) -> str:
        pass

    def create(self, registration: Registration) -> Registration:
        pass

    def from_email(self, email: Email) -> Registration:
        if self._from_email_exception:
            raise self._from_email_exception
        return self._from_email_return

    def save(self, registration: Registration):
        self.saved_registration = registration
