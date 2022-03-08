from domain.identity.email.service import EmailService
from domain.identity.usecase.registration import send_confirmation_email
from domain.identity.value_object.email import Email
from domain.registry import Registry


def test_should_send_confirmation_email():
    email_service = EmailServiceDummy()
    Registry().email_service = email_service
    send_confirmation_email(Email.as_is("aaa@amail.com"), "CONFIRM!!!")
    assert email_service.sent_confirmation_email.str() == "aaa@amail.com" and \
        email_service.sent_confirmation_code == "CONFIRM!!!"


class EmailServiceDummy(EmailService):
    def __init__(self):
        self.sent_confirmation_email = None
        self.sent_confirmation_code = None

    def send_confirmation_email(self, email: Email, confirmation_code: str):
        self.sent_confirmation_email = email
        self.sent_confirmation_code = confirmation_code

    def get_latest_confirmation_code(self, email: Email) -> str:
        pass
