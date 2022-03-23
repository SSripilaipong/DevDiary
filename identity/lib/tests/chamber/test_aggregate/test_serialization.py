from chamber.aggregate import Aggregate, Field


def test_to_dict():
    class MyAggregate(Aggregate):
        my_number: int = Field()

    assert MyAggregate(my_number=1234).to_dict() == {'my_number': 1234}
