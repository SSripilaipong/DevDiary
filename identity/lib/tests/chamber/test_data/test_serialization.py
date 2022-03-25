from chamber.data.field import Field
from chamber.data.model import DataModel
from chamber.flat.string import StringFlat


def test_to_dict():
    class MyModel(DataModel):
        my_number: int = Field()

    assert MyModel(my_number=1234).to_dict() == {'my_number': 1234}


def test_to_dict_with_flat_field():
    class MyModel(DataModel):
        my_number: int = Field()
        my_name: StringFlat = Field()

    assert MyModel(my_number=123, my_name=StringFlat('Hello')).to_dict() == {'my_number': 123, 'my_name': 'Hello'}


def test_should_use_alias():
    class MyModel(DataModel):
        my_number: int = Field("myNumber")

    assert MyModel(my_number=123).to_dict() == {'myNumber': 123}


def test_should_not_serialize_none_serialize_field():
    class MyModel(DataModel):
        my_number: int = Field(serialize=False)

    assert MyModel(my_number=123).to_dict() == {}
