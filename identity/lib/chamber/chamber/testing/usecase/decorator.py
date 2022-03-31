from typing import TypeVar, Callable
from functools import wraps

from chamber.usecase import Usecase

T = TypeVar("T", bound=Callable)


def mock_usecase(usecase_function: Usecase):
    if not isinstance(usecase_function, Usecase):
        raise TypeError("@mock_usecase can only be used with usecase function")

    def decorator(func: T) -> T:
        @wraps(func)
        def wrapper(*args, **kwargs):
            real = usecase_function.get_function()
            usecase_function.override_function(lambda: None)
            try:
                return func(*args, **kwargs)
            finally:
                usecase_function.override_function(real)
        return wrapper
    return decorator
