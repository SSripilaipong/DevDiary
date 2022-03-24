from pytest import raises

from chamber.flat.base import Flat


def test_should_cast_value_when_type_is_wrong():
    Flat("123", int, int)


def test_should_raise_InvalidTypeException_when_type_is_wrong_and_cast_failed():
    with raises(Flat.InvalidTypeException):
        Flat("Hello", int, int)
