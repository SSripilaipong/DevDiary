from typing import TypeVar, Callable
from functools import wraps

from chamber.usecase import Usecase

T = TypeVar("T", bound=Callable)


def mock_usecase(usecase_function: Usecase):
    def decorator(func: T) -> T:
        @wraps(func)
        def wrapper(*args, **kwargs):
            usecase_function.enable_mock()
            try:
                func(*args, **kwargs)
            finally:
                usecase_function.disable_mock()
        return wrapper
    return decorator
