from chamber.flat.string import StringFlat
from domain.identity.value_object.email.exception import EmailMustBeStringException, EmailPatternNotMatchedException


class Email(StringFlat):
    PATTERN = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'

    InvalidTypeException = EmailMustBeStringException
    PatternNotMatchedException = EmailPatternNotMatchedException
