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
    display_name: DisplayName = Field("displayName", getter=True)
    email: Email = Field("email", getter=True)
    is_confirmed: bool = Field("isConfirmed", getter=True)
    _confirmation_code: str = Field("confirmationCode")

    @classmethod
    def create(cls, username: Username, password_hashed: bytes, display_name: DisplayName, email: Email,
               confirmation_code: str) -> 'Registration':
        registration = cls(username=username, password_hashed=password_hashed, display_name=display_name, email=email,
                           is_confirmed=False, _confirmation_code=confirmation_code,
                           _aggregate_version=AggregateVersion.create(0))
        registration._append_message(RegistrationEmailNeededToBeConfirmedEvent(email, confirmation_code))
        return registration

    @command
    def confirm(self, confirmation_code: str):
        """
        :raises:
            RegistrationCanNotBeConfirmedTwiceException
            RegistrationConfirmationCodeNotMatchedException
        """
        if self.is_confirmed:
            raise RegistrationCanNotBeConfirmedTwiceException()
        if self._confirmation_code != confirmation_code:
            raise RegistrationConfirmationCodeNotMatchedException()

        self.is_confirmed = True
        self._append_message(RegistrationConfirmedEvent(self.username, self.display_name, self.email))
