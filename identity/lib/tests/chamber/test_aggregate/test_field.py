from pytest import raises
from chamber.aggregate import Aggregate, Field
from chamber.aggregate.exception import FieldHasNoGetterException


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


def test_should_raise_RuntimeError_when_instantiate_without_type():
    with raises(RuntimeError):
        class _(Aggregate):
            my_number = Field()


def test_should_raise_FieldHasNoGetterException_when_try_to_access_private_field_from_outside():
    class MyAggregate(Aggregate):
        my_number: int = Field()

    obj = MyAggregate(my_number=123)

    with raises(FieldHasNoGetterException):
        print(obj.my_number)


def test_should_be_able_to_access_field_with_getter_from_outside():
    class MyAggregate(Aggregate):
        my_number: int = Field(getter=True)

    assert MyAggregate(my_number=123).my_number == 123
