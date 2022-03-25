from pytest import raises

from chamber.data.field import Field
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


def test_should_raise_AttributeError_when_instantiate_without_required_attribute():
    class MyModel(DataModel):
        my_number: int = Field()

    with raises(AttributeError):
        MyModel()


def test_should_raise_TypeError_when_instantiate_with_wrong_type():
    class MyModel(DataModel):
        my_number: int = Field()

    with raises(TypeError):
        MyModel(my_number="123")


def test_should_raise_RuntimeError_when_instantiate_without_type():
    with raises(RuntimeError):
        class _(DataModel):
            my_number = Field()


def test_should_retrieve_value():
    class MyModel(DataModel):
        my_number: int = Field(getter=True)

    assert MyModel(my_number=123).my_number == 123


def test_should_set_value():
    class MyModel(DataModel):
        my_number: int = Field(getter=True, setter=True)

    data = MyModel(my_number=123)
    data.my_number = 456
    assert data.my_number == 456
