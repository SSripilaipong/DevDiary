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
