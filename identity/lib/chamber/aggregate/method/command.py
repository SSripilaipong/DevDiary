from typing import TypeVar

from chamber.aggregate import Aggregate


class _CommandMethod:
    def __init__(self, instance: Aggregate, func):
        self._instance = instance
        self._func = func

    def __call__(self, *args, **kwargs):
        with self._instance._Aggregate__chamber_field_controller.allow_read_write():
            return self._func(self._instance, *args, **kwargs)


class _Command:
    def __init__(self, func):
        self._func = func

    def __get__(self, instance, owner):
        print(instance)
        return _CommandMethod(instance, self._func)


T = TypeVar("T")


def command(func: T) -> T:
    return _Command(func)
