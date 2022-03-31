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


def test_should_be_able_to_run_real_usecase_outside_mock_area():
    @usecase
    def do_something():
        do_something.done = True

    @mock_usecase(do_something)
    def not_gonna_do_it():
        do_something()

    not_gonna_do_it()
    assert not getattr(do_something, "done", False)

    do_something()
    assert getattr(do_something, "done", False)


def test_should_pass_parameters():
    @usecase
    def do_something():
        pass

    @mock_usecase(do_something)
    def do_mock(value):
        if value == "VALUE":
            do_mock.ok = True

    do_mock("VALUE")
    assert not getattr(do_mock, "ok", False)

    do_something()
    assert getattr(do_something, "ok", False)
