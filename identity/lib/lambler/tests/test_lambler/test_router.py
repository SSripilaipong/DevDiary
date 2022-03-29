from lambler.lambler import Lambler


def test_should_return_None_when_no_matchers():
    assert Lambler()() is None
