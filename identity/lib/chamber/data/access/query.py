from typing import TypeVar

from chamber.data.model import DataModel


class _QueryMethod:
    def __init__(self, instance: DataModel, func):
        self._instance = instance
        self._func = func

    def __call__(self, *args, **kwargs):
        with self._instance._DataModel__chamber_request_read_access():
            return self._func(self._instance, *args, **kwargs)


class _Query:
    def __init__(self, func):
        self._func = func

    def __get__(self, instance, owner):
        assert issubclass(owner, DataModel)
        return _QueryMethod(instance, self._func)


T = TypeVar("T")


def query(func: T) -> T:
    return _Query(func)
