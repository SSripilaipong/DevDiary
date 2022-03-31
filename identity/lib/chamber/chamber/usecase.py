from typing import TypeVar, Callable, Any, Type, Optional

T = TypeVar("T", bound=Callable)


class Usecase:
    def __init__(self, func: Callable):
        self._return_type = self._extract_return_type(func)
        self._func = func
        self._mock = False

    def __call__(self, *args, **kwargs) -> Any:
        if not self._mock:
            return self._func(*args, **kwargs)

    def enable_mock(self):
        self._mock = True

    def disable_mock(self):
        self._mock = False

    def _extract_return_type(self, func: Callable) -> Optional[Type]:
        annotations = getattr(func, "__annotations__", {})
        if "return" not in annotations:
            raise TypeError("Usecase should have a return type.")
        # TODO: implement this


def usecase(func: T) -> T:
    return Usecase(func)
