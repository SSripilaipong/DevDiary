from pytest import raises

from chamber.flat.base import Flat


def test_should_cast_value_when_type_is_wrong():
    Flat("123", int, int)


def test_should_raise_CastingFailedException_when_type_is_wrong_and_cast_failed():
    with raises(Flat.CastingFailedException):
        Flat("Hello", int, int)


def test_should_raise_InvalidTypeException_when_type_is_wrong_and_no_cast_function():
    with raises(Flat.InvalidTypeException):
        Flat("Hello", int)


def test_should_raise_CastingFailedException_when_type_is_still_wrong_after_casting():
    with raises(Flat.CastingFailedException):
        Flat("123", bool, int)


def test_should_accept_any_value_when_create_with_as_is():
    Flat.as_is("Hello")
