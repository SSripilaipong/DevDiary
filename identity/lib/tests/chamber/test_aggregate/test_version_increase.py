from chamber.aggregate.version_increase import AggregateVersionIncrease


def test_should_allow_creating_version_increase_at_least_0():
    AggregateVersionIncrease(0)
    AggregateVersionIncrease(123)
