from pytest import raises

from chamber.aggregate import Field
from chamber.data.model import DataModel


def test_should_instantiate_model_with_fields():
    class MyModel(DataModel):
        my_number: int = Field()
        my_string: str = Field()

    MyModel(my_number=123, my_string="Copy Paste Engineer")


def test_should_raise_AttributeError_when_instantiate_with_unknown_attribute():
    class MyModel(DataModel):
        pass

    with raises(AttributeError):
        MyModel(something=1234)
