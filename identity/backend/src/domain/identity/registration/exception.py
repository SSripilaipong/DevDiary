class EmailAlreadyRegisteredException(Exception):
    pass


class RegistrationNotFoundException(Exception):
    pass


class RegistrationCanNotBeConfirmedTwiceException(Exception):
    pass


class RegistrationConfirmationCodeNotMatchedException(Exception):
    pass
