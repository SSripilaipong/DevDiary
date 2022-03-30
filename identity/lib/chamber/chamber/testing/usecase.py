from typing import TypeVar, Callable
from functools import wraps


T = TypeVar("T", bound=Callable)
U = TypeVar("U", bound=Callable)


def mock_usecase(usecase_function: U):
    def decorator(func: T) -> T:
        @wraps(func)
        def wrapper(*args, **kwargs):
            pass
        return wrapper
    return decorator
