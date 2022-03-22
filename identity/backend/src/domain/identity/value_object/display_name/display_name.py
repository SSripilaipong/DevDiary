import string

from chamber.flat.string import StringFlat
from domain.identity.value_object.display_name.exception import (
    DisplayNameMustBeStringException, DisplayNameContainsInvalidCharacterException, DisplayNameTooLongException,
    DisplayNameTooShortException,
)


class DisplayName(StringFlat):
    MIN_LENGTH = 4
    MAX_LENGTH = 16
    VALID_CHARACTERS = string.digits + string.ascii_lowercase + string.ascii_uppercase + ' #%(),-.?@_~'

    InvalidTypeException = DisplayNameMustBeStringException
    TooShortException = DisplayNameTooShortException
    TooLongException = DisplayNameTooLongException
    ContainsInvalidCharactersException = DisplayNameContainsInvalidCharacterException
