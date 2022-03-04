import string


_VALID_CHARACTERS = string.digits + string.ascii_lowercase + string.ascii_uppercase


class Username:
    def __init__(self, username: str):
        self._username = username

    @classmethod
    def create(cls, username: str) -> 'Username':
        """
        :raises:
            UsernameMustBeStringException
            UsernameContainsInvalidCharacterException
            UsernameTooShortException
            UsernameTooLongException
        """
        if not isinstance(username, str):
            raise UsernameMustBeStringException()
        if len(username) < 4:
            raise UsernameTooShortException()
        if len(username) > 16:
            raise UsernameTooLongException()
        for character in username:
            if character not in _VALID_CHARACTERS:
                raise UsernameContainsInvalidCharacterException()
        return cls(username)

    def str(self) -> str:
        return self._username

    def __eq__(self, other) -> bool:
        if type(self) != type(other):
            return False
        assert isinstance(other, Username)
        return self._username == other._username

    def __hash__(self):
        return self._username.__hash__()


class InvalidUsernameException(Exception):
    pass


class UsernameMustBeStringException(InvalidUsernameException):
    pass


class UsernameContainsInvalidCharacterException(InvalidUsernameException):
    pass


class UsernameTooShortException(InvalidUsernameException):
    pass


class UsernameTooLongException(InvalidUsernameException):
    pass
