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


def test_should_allow_config_MAX_VALUE():
    class MyFlat(IntegerFlat):
        MAX_VALUE = 9

    assert MyFlat(9).int() == 9

    with raises(MyFlat.TooHighException):
        MyFlat(10)


def test_should_raise_TypeError_when_config_MAX_VALUE_with_non_integer():
    with raises(TypeError):
        class MyFlat(IntegerFlat):
            MAX_VALUE = 5.9


def test_should_support_negative_value():
    class MyFlat(IntegerFlat):
        pass

    assert MyFlat(-999).int() == -999


def test_should_cast_to_integer():
    class MyFlat(IntegerFlat):
        CAST = int

    assert MyFlat('-999').int() == -999


def test_should_create_as_is():
    class MyFlat(IntegerFlat):
        MAX_VALUE = 0

    assert MyFlat.as_is(9999).int() == 9999


def test_should_support_equal_operator():
    assert IntegerFlat(1) == IntegerFlat(1)


def test_should_support_less_than_operator():
    assert IntegerFlat(1) < IntegerFlat(2)


def test_should_support_less_than_or_equal_operator():
    assert IntegerFlat(1) <= IntegerFlat(2)
    assert IntegerFlat(1) <= IntegerFlat(1)


def test_should_support_greater_than_operator():
    assert IntegerFlat(2) > IntegerFlat(-999)


def test_should_support_greater_than_or_equal_operator():
    assert IntegerFlat(2) >= IntegerFlat(-999)
    assert IntegerFlat(-999) >= IntegerFlat(-999)


def test_should_raise_TypeError_for_comparison_with_different_type():
    class MyFlat(IntegerFlat):
        pass

    with raises(TypeError):
        _ = IntegerFlat(2) == 2

    with raises(TypeError):
        _ = IntegerFlat(2) == MyFlat(2)

    with raises(TypeError):
        _ = IntegerFlat(2) < 2

    with raises(TypeError):
        _ = IntegerFlat(2) <= MyFlat(2)

    with raises(TypeError):
        _ = IntegerFlat(2) > 2

    with raises(TypeError):
        _ = IntegerFlat(2) >= MyFlat(2)
