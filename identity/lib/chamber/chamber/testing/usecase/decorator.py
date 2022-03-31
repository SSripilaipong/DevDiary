from typing import TypeVar, Callable
from functools import wraps

from chamber.testing.usecase.mocker import UsecaseMocker
from chamber.usecase import Usecase

T = TypeVar("T", bound=Callable)


def mock_usecase(usecase_function: Usecase):
    if not isinstance(usecase_function, Usecase):
        raise TypeError("@mock_usecase can only be used with usecase function")

    def decorator(func: T) -> T:
        @wraps(func)
        def wrapper(*args, **kwargs):
            real = usecase_function.get_function()
            mocker = UsecaseMocker(usecase_function)
            usecase_function.override_function(mocker)
            try:
                result = func(*args, **kwargs)
                mocker.raise_unused_mock()
                return result
            finally:
                usecase_function.override_function(real)
        return wrapper
    return decorator
