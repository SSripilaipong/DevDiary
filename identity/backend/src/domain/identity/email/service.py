from abc import ABC, abstractmethod

from domain.identity.value_object.email import Email


class EmailService(ABC):
    @abstractmethod
    def send_confirmation_email(self, email: Email, confirmation_code: str):
        pass

    @abstractmethod
    def get_latest_confirmation_code(self, email: Email) -> str:
        """
        :raises:
            ConfirmationEmailNotFoundException
        """
