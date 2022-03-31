from pytest import raises

from chamber import usecase
from chamber.testing import mock_usecase, when


def test_should_not_call_real_usecase_when_mocking():
    @usecase
    def do_something() -> None:
        do_something.done = True

    @mock_usecase(do_something)
    def not_gonna_do_it():
        do_something()

    not_gonna_do_it()
    assert not getattr(do_something, "done", False)


def test_should_run_the_test_function():
    @usecase
    def do_something() -> None:
        pass

    @mock_usecase(do_something)
    def not_gonna_do_it():
        not_gonna_do_it.done = True

    not_gonna_do_it()
    assert getattr(not_gonna_do_it, "done", False)


def test_should_be_able_to_run_real_usecase_outside_mock_area():
    @usecase
    def do_something() -> None:
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
    def do_something() -> None:
        pass

    @mock_usecase(do_something)
    def do_mock(value):
        if value == "VALUE":
            do_mock.ok = True

    do_mock("VALUE")
    assert getattr(do_mock, "ok", False)


def test_should_disable_mock_whether_error_occur_or_not():
    @usecase
    def do_something() -> None:
        do_something.done = True

    class SomeException(Exception):
        pass

    @mock_usecase(do_something)
    def do_mock():
        do_something()
        raise SomeException()

    with raises(SomeException):
        do_mock()
    assert not getattr(do_something, "done", False)

    do_something()
    assert getattr(do_something, "done", False)


def test_should_return_value():
    @usecase
    def do_something() -> None:
        pass

    @mock_usecase(do_something)
    def do_mock():
        return 123

    assert do_mock() == 123


def test_should_raise_TypeError_when_type_is_not_Usecase():
    def not_usecase():
        pass

    with raises(TypeError):
        @mock_usecase(not_usecase)
        def do_mock():
            pass


def test_should_return_with_the_instructed_value():
    @usecase
    def do_something() -> int:
        return 123

    @mock_usecase(do_something)
    def do_mock():
        when(do_something()).then_return(999)
        do_mock.return_value = do_something()

    do_mock()
    assert do_mock.return_value == 999


def test_should_raise_TypeError_when_using_when_not_using_when_with_mocked_usecase():
    @usecase
    def do_something() -> None:
        pass

    with raises(TypeError):
        when(do_something())
