from pytest import raises

from chamber.flat.integer import IntegerFlat


def test_should_create_IntegerFlat():
    class MyFlat(IntegerFlat):
        pass
    assert MyFlat(123).int() == 123


def test_should_allow_config_MIN_VALUE():
    class MyFlat(IntegerFlat):
        MIN_VALUE = 5

    assert MyFlat(5).int() == 5

    with raises(MyFlat.TooLowException):
        MyFlat(4)


def test_should_raise_TypeError_when_config_MIN_VALUE_with_float():
    with raises(TypeError):
        class MyFlat(IntegerFlat):
            MIN_VALUE = 5.9
