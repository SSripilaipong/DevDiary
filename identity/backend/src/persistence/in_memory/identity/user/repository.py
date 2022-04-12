from typing import Dict, List

from chamber.message import Message
from domain.identity.user.exception import UsernameAlreadyRegisteredException, UserNotFoundException
from domain.identity.user.repository import AllUsers
from domain.identity.user.user import User
from domain.identity.value_object.username import Username
from domain.registry import Registry


class AllUsersInMemory(AllUsers):
    def __init__(self, users: Dict[Username, User] = None, topic_prefix: str = ""):
        self._users = users or dict()
        self._topic_prefix = topic_prefix

    def create(self, user: User) -> User:
        """
        :raises:
            UsernameAlreadyRegisteredException
        """
        if user.username in self._users:
            raise UsernameAlreadyRegisteredException()
        self._store_and_handle_outbox(user)
        return user

    def from_username(self, username: Username) -> User:
        """
        :raises:
            UserNotFoundException
        """
        if username not in self._users:
            raise UserNotFoundException()
        return self._users[username]

    def _store_and_handle_outbox(self, user: User):
        outbox = user.get_aggregate_outbox_messages()
        user.clear_aggregate_outbox_messages()
        self._users[user.username] = user
        self._handle_outbox(outbox)

    def _handle_outbox(self, outbox: List[Message]):
        message_bus = Registry().message_bus
        for message in outbox:
            message_bus.publish(f"{self._topic_prefix}{message.__class__.__name__}", message)
