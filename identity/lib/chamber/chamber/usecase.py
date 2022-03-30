from typing import TypeVar, Callable, Any

T = TypeVar("T", bound=Callable)


class Usecase:
    def __init__(self, func: Callable):
        self._func = func
        self._mock = False

    def __call__(self, *args, **kwargs) -> Any:
        if not self._mock:
            return self._func(*args, **kwargs)

    def enable_mock(self):
        self._mock = True

    def disable_mock(self):
        self._mock = False


def usecase(func: T) -> T:
    return Usecase(func)
