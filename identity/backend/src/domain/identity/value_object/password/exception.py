class InvalidPasswordException(Exception):
    pass


class PasswordMustBeStringException(InvalidPasswordException):
    pass


class PasswordMustContainRequiredCharactersException(InvalidPasswordException):
    pass


class PasswordTooShortException(InvalidPasswordException):
    pass


class PasswordTooLongException(InvalidPasswordException):
    pass
