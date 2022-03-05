import string

from chamber.flat.string import StringFlat
from domain.identity.value_object.password.exception import (
    PasswordMustBeStringException, PasswordMustContainRequiredCharactersException, PasswordTooShortException,
    PasswordTooLongException,
)


class Password(StringFlat):
    MIN_LENGTH = 8
    MAX_LENGTH = 64
    REQUIRED_CHARACTER_SETS = [string.ascii_lowercase, string.ascii_uppercase, string.digits]

    InvalidTypeException = PasswordMustBeStringException
    TooShortException = PasswordTooShortException
    TooLongException = PasswordTooLongException
    RequiredCharactersMissingException = PasswordMustContainRequiredCharactersException
