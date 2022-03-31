from pytest import raises
from chamber.usecase import usecase


def test_should_run_usecase_function():
    @usecase
    def do_something() -> int:
        do_something.done = True
        return 0

    do_something()
    assert getattr(do_something, "done", False)


def test_should_raise_TypeError_when_return_type_is_not_annotated():
    with raises(TypeError):
        @usecase
        def do_something():
            return 0


def test_should_raise_TypeError_when_parameter_annotation_missing():
    with raises(TypeError):
        @usecase
        def do_something(a) -> None:
            pass


def test_should_raise_TypeError_when_parameter_annotation_is_not_a_type():
    with raises(TypeError):
        @usecase
        def do_something(a: 123) -> None:
            pass


def test_should_raise_TypeError_when_calling_with_wrong_type_parameter():
    @usecase
    def do_something(a: int) -> None:
        pass

    with raises(TypeError):
        do_something("Hello")


def test_should_raise_TypeError_when_calling_with_wrong_type_parameters():
    @usecase
    def do_something(a: int, b: str, c: bool) -> None:
        pass

    with raises(TypeError):
        do_something(123, True, "Hello")


def test_should_raise_TypeError_when_calling_with_wrong_type_keyword_parameters():
    @usecase
    def do_something(a: int, b: str) -> None:
        pass

    with raises(TypeError):
        do_something(123, b=True)


def test_should_raise_TypeError_when_parameter_missing_and_no_default_value():
    @usecase
    def do_something(a: int, b: str) -> None:
        pass

    with raises(TypeError):
        do_something(123)
