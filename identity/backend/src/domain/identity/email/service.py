from abc import ABC, abstractmethod


class EmailService(ABC):
    @abstractmethod
    def send_confirmation_email(self, email: str, confirmation_code: str):
        pass

    @abstractmethod
    def get_latest_confirmation_code(self, email: str) -> str:
        """
        :raises:
            ConfirmationEmailNotFoundException
        """
