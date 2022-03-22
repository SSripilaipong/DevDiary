from pytest import raises
from chamber.aggregate import Aggregate, Field


def test_should_instantiate_aggregate_with_fields():
    class MyAggregate(Aggregate):
        my_number: int = Field()
        my_string: str = Field()

    MyAggregate(my_number=123, my_string="Copy Paste Engineer")


def test_should_raise_TypeError_when_instantiate_with_wrong_type():
    class MyAggregate(Aggregate):
        my_number: int = Field()

    with raises(TypeError):
        MyAggregate(my_number="123")


def test_should_raise_TypeError_when_instantiate_without_type():
    with raises(TypeError):
        class _(Aggregate):
            my_number: int = Field()
