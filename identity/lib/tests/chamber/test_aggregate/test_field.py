from chamber.aggregate import Aggregate, Field


def test_should_instantiate_aggregate_with_fields():
    class MyAggregate(Aggregate):
        my_number: int = Field()
        my_string: str = Field()

    MyAggregate(my_number=123, my_string="Copy Paste Engineer")
