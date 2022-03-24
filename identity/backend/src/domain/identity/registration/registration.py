from chamber.aggregate import Aggregate, Field, command
from chamber.aggregate.version import AggregateVersion
from domain.identity.registration.event.confirmation_needed import RegistrationEmailNeededToBeConfirmedEvent
from domain.identity.registration.event.confirmed import RegistrationConfirmedEvent
from domain.identity.registration.exception import (
    RegistrationCanNotBeConfirmedTwiceException, RegistrationConfirmationCodeNotMatchedException,
)
from domain.identity.value_object.display_name import DisplayName
from domain.identity.value_object.email import Email
from domain.identity.value_object.username import Username


class Registration(Aggregate):
    username: Username = Field("username", getter=True)
    password_hashed: bytes = Field("passwordHashed", getter=True)

    def __init__(self, username: Username, password_hashed: bytes, display_name: DisplayName, email: Email, is_confirmed: bool,
                 confirmation_code: str, _version: AggregateVersion):
        super().__init__(username=username, password_hashed=password_hashed, _aggregate_version=_version)
        self._display_name = display_name
        self._email = email
        self._is_confirmed = is_confirmed
        self._confirmation_code = confirmation_code

    @classmethod
    def create(cls, username: Username, password_hashed: bytes, display_name: DisplayName, email: Email,
               confirmation_code: str) -> 'Registration':
        registration = cls(username, password_hashed, display_name, email,
                           is_confirmed=False, confirmation_code=confirmation_code, _version=AggregateVersion.create(0))
        registration._append_message(
            RegistrationEmailNeededToBeConfirmedEvent(registration._email, registration._confirmation_code))
        return registration

    @command
    def confirm(self, confirmation_code: str):
        """
        :raises:
            RegistrationCanNotBeConfirmedTwiceException
            RegistrationConfirmationCodeNotMatchedException
        """
        if self._is_confirmed:
            raise RegistrationCanNotBeConfirmedTwiceException()
        if self._confirmation_code != confirmation_code:
            raise RegistrationConfirmationCodeNotMatchedException()

        self._is_confirmed = True
        self._append_message(RegistrationConfirmedEvent(self.username, self._display_name, self._email))

    @property
    def display_name(self) -> DisplayName:
        return self._display_name

    @property
    def email(self) -> Email:
        return self._email

    def is_confirmed(self) -> bool:
        return self._is_confirmed
