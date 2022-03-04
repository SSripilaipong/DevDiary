from typing import Dict

from chamber.message import Message
from domain.identity.value_object.username import Username


class UserCreatedEvent(Message):
    def __init__(self, username: Username, display_name: str, email: str):
        self._username = username
        self._display_name = display_name
        self._email = email

    def _body_to_dict(self) -> Dict:
        return {
            "username": self._username.str(),
            "display_name": self._display_name,
            "email": self._email,
        }

    @classmethod
    def _body_from_dict(cls, obj: Dict) -> 'UserCreatedEvent':
        return cls(
            username=Username.create(obj.get('username')),
            display_name=obj.get('display_name'),
            email=obj.get('email'),
        )

