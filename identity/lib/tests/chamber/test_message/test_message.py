from pytest import raises

from chamber.data.exception import DeserializationFailedException
from chamber.data.field import Field
from chamber.message import Message


def test_should_serialize_to_dict_with_name_and_body():
    class MyMessage(Message):
        my_number: int = Field()
        my_string: str = Field()

    data = MyMessage(my_number=123, my_string='abc').to_dict()
    assert data == {"name": "MyMessage", "body": {"my_number": 123, "my_string": "abc"}}


def test_should_deserialize_from_dict():
    class MyMessage(Message):
        my_number: int = Field(getter=True)
        my_string: str = Field(getter=True)

    msg = MyMessage.from_dict({"name": "MyMessage", "body": {"my_number": 123, "my_string": "abc"}})
    assert msg.my_number == 123 and msg.my_string == 'abc'


def test_should_raise_DeserializationFailedException_when_deserializing_data_with_different_name():
    class MyMessage(Message):
        my_number: int = Field(getter=True)
        my_string: str = Field(getter=True)

    with raises(DeserializationFailedException):
        MyMessage.from_dict({"name": "NotMyMessage", "body": {"my_number": 123, "my_string": "abc"}})
