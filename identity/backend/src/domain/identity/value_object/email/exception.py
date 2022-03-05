class InvalidEmailException(Exception):
    pass


class EmailMustBeStringException(InvalidEmailException):
    pass


class EmailPatternNotMatchedException(InvalidEmailException):
    pass
