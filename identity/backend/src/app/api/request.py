from chamber.data.field import Field
from chamber.data.model import DataModel

from domain.identity.value_object.display_name import DisplayName
from domain.identity.value_object.email import Email
from domain.identity.value_object.password import Password
from domain.identity.value_object.username import Username


class RegistrationRequest(DataModel):
    username: Username = Field(getter=True)
    password: Password = Field(getter=True)
    display_name: DisplayName = Field("displayName", getter=True)
    email: Email = Field(getter=True)
