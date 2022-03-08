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


class AllRegistrationsDummy(AllRegistrations):
    def __init__(self, from_email_return=None):
        self._from_email_return = from_email_return

    def generate_confirmation_code(self) -> str:
        pass

    def create(self, registration: Registration) -> Registration:
        pass

    def from_email(self, email: Email) -> Registration:
        return self._from_email_return

    def save(self, registration: Registration):
        pass

