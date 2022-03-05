from typing import Dict

from chamber.message import Message
from domain.identity.value_object.email import Email


class RegistrationEmailNeededToBeConfirmedEvent(Message):
    def __init__(self, email: Email, confirmation_code: str):
        self._email = email
        self._confirmation_code = confirmation_code

    @property
    def email(self) -> Email:
        return self._email

    @property
    def confirmation_code(self) -> str:
        return self._confirmation_code

    def _body_to_dict(self) -> Dict:
        return {
            "email": self._email.str(),
            "confirmation_code": self._confirmation_code,
        }

    @classmethod
    def _body_from_dict(cls, obj: Dict) -> 'RegistrationEmailNeededToBeConfirmedEvent':
        return cls(
            email=Email.as_is(obj.get('email')),
            confirmation_code=obj.get('confirmation_code'),
        )
