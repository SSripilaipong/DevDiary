from pytest import raises
from chamber.flat.string import StringFlat


def test_should_create_StringFlat():
    assert NoConstraint("abc123@#$").str() == "abc123@#$"


def test_should_override_exception_with_MyInvalidTypeException1_and_MyInvalidTypeException2():
    with raises(MyInvalidTypeException1):
        ExceptionOverrode1(123)
    with raises(MyInvalidTypeException2):
        ExceptionOverrode2(123)


def test_should_cast_to_string():
    assert WillCast(123).str() == "123"


def test_should_raise_CastingFailedException():
    with raises(WillCastAndFail.CastingFailedException):
        WillCastAndFail(123)


def test_should_cast_and_raise_CastingFailedException():
    with raises(WillCastAndReturnSomethingElse.CastingFailedException):
        WillCastAndReturnSomethingElse(123)


def test_should_raise_TooShortException():
    with raises(WithConstraints.TooShortException):
        WithConstraints("a")


def test_should_raise_TooLongException():
    with raises(WithConstraints.TooLongException):
        WithConstraints("aaaaaaaaaaaaaaaa")


def test_should_raise_ContainsInvalidCharactersException():
    with raises(WithConstraints.ContainsInvalidCharactersException):
        WithConstraints("bbb")


class NoConstraint(StringFlat):
    pass


class MyInvalidTypeException1(Exception):
    pass


class MyInvalidTypeException2(Exception):
    pass


class ExceptionOverrode1(StringFlat):
    InvalidTypeException = MyInvalidTypeException1


class ExceptionOverrode2(StringFlat):
    InvalidTypeException = MyInvalidTypeException2


class WillCast(StringFlat):
    CAST = str


class WillCastAndFail(StringFlat):
    CAST = lambda x: 0/0


class WillCastAndReturnSomethingElse(StringFlat):
    CAST = lambda x: 123


class WithConstraints(StringFlat):
    MIN_LENGTH = 3
    MAX_LENGTH = 5
    VALID_CHARACTERS = "a"
