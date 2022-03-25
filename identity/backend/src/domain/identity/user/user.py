from chamber.aggregate import Aggregate, Field
from chamber.aggregate.version import AggregateVersion
from domain.identity.user.event.created import UserCreatedEvent
from domain.identity.value_object.display_name import DisplayName
from domain.identity.value_object.email import Email
from domain.identity.value_object.username import Username


class User(Aggregate):
    username: Username = Field(getter=True)

    def __init__(self, username: Username, password_hashed: bytes, display_name: DisplayName, email: Email,
                 _version: AggregateVersion):
        super().__init__(username=username, _aggregate_version=_version)
        self._password_hashed = password_hashed
        self._display_name = display_name
        self._email = email

    @classmethod
    def create(cls, username: Username, password_hashed: bytes, display_name: DisplayName, email: Email) -> 'User':
        user = cls(username, password_hashed, display_name, email, AggregateVersion(0))
        user._append_message(UserCreatedEvent(user.username, user._display_name, user._email))
        return user

    @property
    def password_hashed(self) -> bytes:
        return self._password_hashed

    @property
    def display_name(self) -> DisplayName:
        return self._display_name
