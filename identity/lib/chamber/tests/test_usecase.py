from chamber import usecase


def test_should_run_usecase_function():
    @usecase
    def do_something():
        do_something.done = True

    do_something()
    assert getattr(do_something, "done", False)
