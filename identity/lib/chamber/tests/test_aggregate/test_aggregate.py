from chamber.aggregate import Aggregate
from chamber.aggregate.version import AggregateVersion
from chamber.data.field import Field


def test_should_allow_passing_version_when_using_from_dict():
    class MyAggregate(Aggregate):
        my_string: str = Field()

    aggregate = MyAggregate.from_dict({"my_string": "Hello"}, _aggregate_version=AggregateVersion(8))
    assert aggregate.aggregate_version.int() == 8
