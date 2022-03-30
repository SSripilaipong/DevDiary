from chamber import usecase
from chamber.testing import mock_usecase


def test_should_not_call_real_usecase_when_mocking():
    @usecase
    def do_something():
        do_something.done = True

    @mock_usecase(do_something)
    def not_gonna_do_it():
        do_something()

    not_gonna_do_it()
    assert not getattr(do_something, "done", False)


def test_should_run_the_test_function():
    @usecase
    def do_something():
        pass

    @mock_usecase(do_something)
    def not_gonna_do_it():
        not_gonna_do_it.done = True

    not_gonna_do_it()
    assert getattr(not_gonna_do_it, "done", False)
