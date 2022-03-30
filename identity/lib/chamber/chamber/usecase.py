from typing import TypeVar, Callable


T = TypeVar("T", bound=Callable)


def usecase(func: T) -> T:
    pass
