class InvalidDisplayNameException(Exception):
    pass


class DisplayNameMustBeStringException(InvalidDisplayNameException):
    pass


class DisplayNameContainsInvalidCharacterException(InvalidDisplayNameException):
    pass


class DisplayNameTooShortException(InvalidDisplayNameException):
    pass


class DisplayNameTooLongException(InvalidDisplayNameException):
    pass
