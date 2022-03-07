from chamber.flat.string import StringFlat
from domain.identity.value_object.email.exception import EmailMustBeStringException, EmailPatternNotMatchedException


class Email(StringFlat):
    PATTERN = r"^[a-zA-Z0-9_+&*-]+(?:\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,7}$"

    InvalidTypeException = EmailMustBeStringException
    PatternNotMatchedException = EmailPatternNotMatchedException
