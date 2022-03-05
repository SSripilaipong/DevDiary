from abc import ABC, abstractmethod

from domain.identity.registration.registration import Registration
from domain.identity.value_object.email import Email


class AllRegistrations(ABC):
    @abstractmethod
    def generate_confirmation_code(self) -> str:
        pass

    @abstractmethod
    def create(self, registration: Registration) -> Registration:
        """
        :raises:
            EmailAlreadyRegisteredException
            UsernameAlreadyRegisteredException
        """

    @abstractmethod
    def from_email(self, email: Email) -> Registration:
        """
        :raises:
            RegistrationNotFoundException
        """

    @abstractmethod
    def save(self, registration: Registration):
        """
        :raises:
            EntityOutdated
        """
