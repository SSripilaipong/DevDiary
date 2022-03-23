from pytest import raises

from chamber.aggregate import Aggregate, Field
from chamber.flat.string import StringFlat


def test_should_create_aggregate_from_dict():
    class MyAggregate(Aggregate):
        my_number: int = Field(getter=True)

    obj = MyAggregate.from_dict({"my_number": 123})
    assert obj.my_number == 123


def test_should_convert_primitive_to_flat():
    class MyAggregate(Aggregate):
        my_string: StringFlat = Field(getter=True)

    obj = MyAggregate.from_dict({"my_string": "Copy Paste Engineer"})
    assert obj.my_string == StringFlat("Copy Paste Engineer")


def test_should_create_aggregate_with_field_in_alias_name():
    class MyAggregate(Aggregate):
        my_number: int = Field("myNumber", getter=True)

    obj = MyAggregate.from_dict({"myNumber": 123})
    assert obj.my_number == 123


def test_should_raise_AttributeError_when_field_name_is_unknown():
    class MyAggregate(Aggregate):
        my_number: int = Field()

    with raises(AttributeError):
        MyAggregate.from_dict({"my_number": 123, "Copy": "Paste"})


def test_should_raise_TypeError_when_type_is_wrong_and_no_deserialize_function():
    class MyAggregate(Aggregate):
        my_string: str = Field()

    with raises(TypeError):
        MyAggregate.from_dict({"my_string": 123})
