from typing import List, Dict

from domain.identity.email.exception import ConfirmationEmailNotFoundException
from domain.identity.email.service import EmailService
from domain.identity.value_object.email import Email


class EmailServiceInMemory(EmailService):
    def __init__(self):
        self._confirmation_code_box: Dict[Email, List[str]] = {}

    def send_confirmation_email(self, email: Email, confirmation_code: str):
        self._confirmation_code_box[email] = self._confirmation_code_box.get(email, []) + [confirmation_code]

    def get_latest_confirmation_code(self, email: Email) -> str:
        """
        :raises:
            ConfirmationEmailNotFoundException
        """
        code_box = self._confirmation_code_box.get(email, [])
        if len(code_box) == 0:
            raise ConfirmationEmailNotFoundException()
        return code_box[-1]
