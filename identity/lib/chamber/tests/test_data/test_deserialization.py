from pytest import raises

from chamber.data.exception import DeserializationFailedException
from chamber.data.field import Field
from chamber.data.model import DataModel
from chamber.flat.string import StringFlat


def test_should_create_aggregate_from_dict():
    class MyModel(DataModel):
        my_number: int = Field(getter=True)

    obj = MyModel.from_dict({"my_number": 123})
    assert obj.my_number == 123


def test_should_convert_primitive_to_flat():
    class MyModel(DataModel):
        my_string: StringFlat = Field(getter=True)

    obj = MyModel.from_dict({"my_string": "Copy Paste Engineer"})
    assert obj.my_string == StringFlat("Copy Paste Engineer")


def test_should_create_aggregate_with_field_in_alias_name():
    class MyModel(DataModel):
        my_number: int = Field("myNumber", getter=True)

    obj = MyModel.from_dict({"myNumber": 123})
    assert obj.my_number == 123


def test_should_raise_DeserializationFailedException_when_field_name_is_unknown():
    class MyModel(DataModel):
        my_number: int = Field()

    with raises(DeserializationFailedException):
        MyModel.from_dict({"my_number": 123, "Copy": "Paste"})


def test_should_raise_DeserializationFailedException_when_type_is_wrong_and_no_deserialize_function():
    class MyModel(DataModel):
        my_string: str = Field()

    with raises(DeserializationFailedException):
        MyModel.from_dict({"my_string": 123})


def test_should_raise_DeserializationFailedException_when_deserialize_function_raise_any_error():
    class MyData:
        @classmethod
        def deserialize(cls, value):
            raise Exception()

    class MyModel(DataModel):
        my_data: MyData = Field()

    with raises(DeserializationFailedException):
        MyModel.from_dict({"my_data": 123})
