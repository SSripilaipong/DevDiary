from typing import TypeVar, Type

from chamber.aggregate import Aggregate


class _QueryMethod:
    def __init__(self, instance: Aggregate, func):
        self._instance = instance
        self._func = func

    def __call__(self, *args, **kwargs):
        with self._instance._field_controller.allow_read():
            return self._func(self._instance, *args, **kwargs)


class _Query:
    def __init__(self, func):
        self._func = func

    def __get__(self, instance, owner):
        print(instance)
        return _QueryMethod(instance, self._func)


T = TypeVar("T")


def query(func: T) -> T:
    return _Query(func)
