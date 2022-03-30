from chamber import usecase
from chamber.testing import mock_usecase


def test_should_not_call_real_usecase_when_mocking():
    @usecase
    def do_something():
        do_something.done = True

    @mock_usecase(do_something)
    def not_gonna_do_it():
        do_something()

    assert not getattr(do_something, "done", False)
