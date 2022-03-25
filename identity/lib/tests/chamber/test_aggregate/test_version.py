from pytest import raises

from chamber.aggregate.exception import InvalidAggregateVersionException
from chamber.aggregate.version import AggregateVersion


def test_should_allow_creating_AggregateVersion():
    AggregateVersion(123)


def test_should_raise_InvalidAggregateVersionException_when_create_with_negative_value():
    with raises(InvalidAggregateVersionException):
        AggregateVersion(-1)
