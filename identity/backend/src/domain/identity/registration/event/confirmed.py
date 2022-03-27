from chamber.data import Field
from chamber.message import Message
from domain.identity.value_object.display_name import DisplayName
from domain.identity.value_object.email import Email
from domain.identity.value_object.username import Username


class RegistrationConfirmedEvent(Message):
    username: Username = Field(getter=True)
    display_name: DisplayName = Field(getter=True)
    email: Email = Field(getter=True)

    def __init__(self, username: Username, display_name: DisplayName, email: Email):
        super().__init__(username=username, display_name=display_name, email=email)
