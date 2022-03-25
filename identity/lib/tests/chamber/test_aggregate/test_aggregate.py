from pytest import raises

from chamber.aggregate import Aggregate
from chamber.data.field import Field


def test_should_instantiate_aggregate_with_fields():
    class MyAggregate(Aggregate):
        my_number: int = Field()
        my_string: str = Field()

    MyAggregate(my_number=123, my_string="Copy Paste Engineer")


def test_should_raise_AttributeError_when_instantiate_with_unknown_attribute():
    class MyAggregate(Aggregate):
        pass

    with raises(AttributeError):
        MyAggregate(something=1234)


def test_should_raise_AttributeError_when_instantiate_without_required_attribute():
    class MyAggregate(Aggregate):
        my_number: int = Field()

    with raises(AttributeError):
        MyAggregate()


def test_should_raise_TypeError_when_instantiate_with_wrong_type():
    class MyAggregate(Aggregate):
        my_number: int = Field()

    with raises(TypeError):
        MyAggregate(my_number="123")


def test_should_raise_RuntimeError_when_instantiate_without_type():
    with raises(RuntimeError):
        class _(Aggregate):
            my_number = Field()

