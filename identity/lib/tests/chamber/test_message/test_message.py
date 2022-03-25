from chamber.data.field import Field
from chamber.message import Message


def test_should_serialize_to_dict_with_name_and_body():
    class MyMessage(Message):
        my_number: int = Field()
        my_string: str = Field()

    data = MyMessage(my_number=123, my_string='abc').to_dict()
    assert data == {"name": "MyMessage", "body": {"my_number": 123, "my_string": "abc"}}
