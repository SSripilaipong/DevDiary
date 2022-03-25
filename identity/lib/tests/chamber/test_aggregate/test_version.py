from chamber.aggregate.version import AggregateVersion


def test_should_allow_creating_AggregateVersion():
    AggregateVersion(123)
