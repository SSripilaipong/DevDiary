from chamber.aggregate import Aggregate, Field
from chamber.flat.string import StringFlat


def test_to_dict():
    class MyAggregate(Aggregate):
        my_number: int = Field()

    assert MyAggregate(my_number=1234).to_dict() == {'my_number': 1234}


def test_to_dict_with_flat_field():
    class MyAggregate(Aggregate):
        my_number: int = Field()
        my_name: StringFlat = Field()

    assert MyAggregate(my_number=123, my_name=StringFlat('Hello')).to_dict() == {'my_number': 123, 'my_name': 'Hello'}


def test_should_use_alias():
    class MyAggregate(Aggregate):
        my_number: int = Field("myNumber")

    assert MyAggregate(my_number=123).to_dict() == {'myNumber': 123}
