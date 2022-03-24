from chamber.flat.integer import IntegerFlat


def test_should_create_IntegerFlat():
    class MyFlat(IntegerFlat):
        pass
    assert MyFlat(123).int() == 123
