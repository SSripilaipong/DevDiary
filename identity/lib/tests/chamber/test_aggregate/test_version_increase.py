from pytest import raises

from chamber.aggregate.exception import InvalidAggregateVersionException
from chamber.aggregate.version_increase import AggregateVersionIncrease


def test_should_allow_creating_version_increase_at_least_0():
    AggregateVersionIncrease(0)
    AggregateVersionIncrease(123)


def test_should_raise_InvalidAggregateVersionException_when_create_with_negative_value():
    with raises(InvalidAggregateVersionException):
        AggregateVersionIncrease(-1)


def test_should_raise_InvalidAggregateVersionException_when_create_with_wrong_type():
    with raises(InvalidAggregateVersionException):
        AggregateVersionIncrease("123")

    with raises(InvalidAggregateVersionException):
        AggregateVersionIncrease(123.5)
