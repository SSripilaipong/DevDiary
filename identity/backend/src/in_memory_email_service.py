from typing import List, Dict

from domain.identity.email.exception import ConfirmationEmailNotFoundException
from domain.identity.email.service import EmailService


class EmailServiceInMemory(EmailService):
    def __init__(self):
        self._confirmation_code_box: Dict[str, List[str]] = {}

    def send_confirmation_email(self, email: str, confirmation_code: str):
        self._confirmation_code_box[email] = self._confirmation_code_box.get(email, []) + [confirmation_code]

    def get_latest_confirmation_code(self, email: str) -> str:
        """
        :raises:

            ConfirmationEmailNotFoundException
        """
        code_box = self._confirmation_code_box.get(email, [])
        if len(code_box) == 0:
            raise ConfirmationEmailNotFoundException()
        return code_box[-1]
