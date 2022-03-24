from pytest import raises

from chamber.flat.base import Flat


def test_should_raise_InvalidTypeException_when_type_is_wrong():
    with raises(Flat.InvalidTypeException):
        Flat("Hello", int)
