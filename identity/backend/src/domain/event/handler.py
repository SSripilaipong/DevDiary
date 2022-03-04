from domain.identity.registration.event.confirmation_needed import RegistrationEmailNeededToBeConfirmedEvent
from domain.identity.registration.event.confirmed import RegistrationConfirmedEvent
from domain.identity.usecase.registration import send_confirmation_email
from domain.identity.user.usecase import create_new_user_from_registered_email


def handle_email_needed_confirmation(message: RegistrationEmailNeededToBeConfirmedEvent):
    send_confirmation_email(message.email, message.confirmation_code)


def handle_registration_confirmed(message: RegistrationConfirmedEvent):
    create_new_user_from_registered_email(message.email)
