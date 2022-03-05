class InvalidPasswordException(Exception):
    pass


class PasswordMustBeStringException(InvalidPasswordException):
    pass


class PasswordMustContainRequiredCharacters(InvalidPasswordException):
    pass


class PasswordTooShortException(InvalidPasswordException):
    pass


class PasswordTooLongException(InvalidPasswordException):
    pass
