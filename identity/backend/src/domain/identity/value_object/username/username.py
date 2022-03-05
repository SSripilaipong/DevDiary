import string

from chamber.flat.string import StringFlat
from domain.identity.value_object.username.exception import (
    UsernameMustBeStringException, UsernameContainsInvalidCharacterException, UsernameTooShortException,
    UsernameTooLongException,
)


class Username(StringFlat):
    MIN_LENGTH = 4
    MAX_LENGTH = 16
    VALID_CHARACTERS = string.digits + string.ascii_lowercase + string.ascii_uppercase

    InvalidTypeException = UsernameMustBeStringException
    TooShortException = UsernameTooShortException
    TooLongException = UsernameTooLongException
    ContainsInvalidCharactersException = UsernameContainsInvalidCharacterException
