from typing import Dict

from chamber.message import Message
from domain.identity.value_object.email import Email
from domain.identity.value_object.username import Username


class RegistrationConfirmedEvent(Message):
    def __init__(self, username: Username, display_name: str, email: Email):
        self._username = username
        self._display_name = display_name
        self._email = email

    @property
    def email(self) -> Email:
        return self._email

    def _body_to_dict(self) -> Dict:
        return {
            "username": self._username.str(),
            "display_name": self._display_name,
            "email": self._email.str(),
        }

    @classmethod
    def _body_from_dict(cls, obj: Dict) -> 'RegistrationConfirmedEvent':
        return cls(
            username=Username.create(obj.get('username')),
            display_name=obj.get('display_name'),
            email=Email.as_is(obj.get('email')),
        )
