from abc import ABC, abstractmethod

from domain.identity.user.user import User
from domain.identity.value_object.username import Username


class AllUsers(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        """
        :raises:
            UsernameAlreadyRegisteredException
        """

    @abstractmethod
    def from_username(self, username: Username) -> User:
        """
        :raises:
            UserNotFoundException
        """