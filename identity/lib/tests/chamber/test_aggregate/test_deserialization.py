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
    assert obj.my_string == "Copy Paste Engineer"
