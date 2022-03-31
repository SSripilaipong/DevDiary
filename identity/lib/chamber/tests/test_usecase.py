from pytest import raises
from chamber import usecase


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
