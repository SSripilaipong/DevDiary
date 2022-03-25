from pytest import raises
from chamber.data.field import Field
from chamber.aggregate import Aggregate, query, command
from chamber.aggregate.exception import FieldHasNoGetterException, FieldHasNoSetterException


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


def test_should_be_able_to_access_field_without_getter_from_query_method():
    class MyAggregate(Aggregate):
        my_number: int = Field()

        @query
        def get_my_number(self):
            return self.my_number

    assert MyAggregate(my_number=123).get_my_number() == 123


def test_should_raise_FieldHasNoSetterException_when_try_to_set_value_for_field_without_setter_from_outside():
    class MyAggregate(Aggregate):
        my_number: int = Field()

    obj = MyAggregate(my_number=123)

    with raises(FieldHasNoSetterException):
        obj.my_number = 456


def test_should_be_able_to_set_value_for_field_with_setter_from_outside():
    class MyAggregate(Aggregate):
        my_number: int = Field(getter=True, setter=True)

    obj = MyAggregate(my_number=123)
    obj.my_number = 456

    assert obj.my_number == 456


def test_should_be_able_to_set_value_for_field_without_setter_from_command_method():
    class MyAggregate(Aggregate):
        my_number: int = Field(getter=True)

        @command
        def modify_my_number(self, x):
            self.my_number += x

    obj = MyAggregate(my_number=123)
    obj.modify_my_number(876)

    assert obj.my_number == 999
