from typing import TypeVar, Callable


T = TypeVar("T", bound=Callable)


def mock_usecase(func: T) -> T:
    pass
