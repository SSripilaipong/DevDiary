from chamber.data import Field
from chamber.message import Message
from domain.identity.value_object.email import Email


class RegistrationEmailNeededToBeConfirmedEvent(Message):
    email: Email = Field(getter=True)
    confirmation_code: str = Field("confirmationCode", getter=True)

    def __init__(self, email: Email, confirmation_code: str):
        super().__init__(email=email, confirmation_code=confirmation_code)
