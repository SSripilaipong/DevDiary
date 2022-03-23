from chamber.aggregate import Aggregate, Field


def test_should_create_aggregate_from_dict():
    class MyAggregate(Aggregate):
        my_number: int = Field(getter=True)

    obj = MyAggregate.from_dict({"my_number": 123})
    assert obj.my_number == 123
