from chamber.aggregate import Aggregate
from chamber.aggregate.version import AggregateVersion
from domain.identity.user.event.created import UserCreatedEvent
from domain.identity.value_object.username import Username


class User(Aggregate):
    def __init__(self, username: Username, password_hashed: bytes, display_name: str, email: str,
                 _version: AggregateVersion):
        super().__init__(aggregate_version=_version)
        self._username = username
        self._password_hashed = password_hashed
        self._display_name = display_name
        self._email = email

    @classmethod
    def create(cls, username: Username, password_hashed: bytes, display_name: str, email: str) -> 'User':
        user = cls(username, password_hashed, display_name, email, AggregateVersion.create(0))
        user._append_message(UserCreatedEvent(user._username, user._display_name, user._email))
        return user

    @property
    def password_hashed(self) -> bytes:
        return self._password_hashed

    @property
    def username(self) -> Username:
        return self._username

    @property
    def display_name(self) -> str:
        return self._display_name
