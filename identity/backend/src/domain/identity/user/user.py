from chamber.aggregate import Aggregate, Field
from chamber.aggregate.version import AggregateVersion
from domain.identity.user.event.created import UserCreatedEvent
from domain.identity.value_object.display_name import DisplayName
from domain.identity.value_object.email import Email
from domain.identity.value_object.username import Username


class User(Aggregate):
    username: Username = Field(getter=True)
    password_hashed: bytes = Field("passwordHashed", getter=True)
    display_name: DisplayName = Field("displayName", getter=True)
    email: Email = Field()

    @classmethod
    def create(cls, username: Username, password_hashed: bytes, display_name: DisplayName, email: Email) -> 'User':
        user = cls(username=username, password_hashed=password_hashed, display_name=display_name, email=email,
                   _aggregate_version=AggregateVersion(0))
        user._append_message(UserCreatedEvent(username, display_name, email))
        return user
