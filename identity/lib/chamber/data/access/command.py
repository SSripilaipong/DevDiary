from typing import TypeVar, Type

from chamber.aggregate import Aggregate


class _CommandMethod:
    def __init__(self, instance: Aggregate, owner: Type, func):
        self._instance = instance
        self._owner = owner
        self._func = func

    def __call__(self, *args, **kwargs):
        from chamber.data.model import DataModel
        if issubclass(self._owner, DataModel):
            with self._instance._DataModel__chamber_request_read_write_access():
                return self._func(self._instance, *args, **kwargs)
        with self._instance._Aggregate__chamber_field_controller.allow_read_write():
            return self._func(self._instance, *args, **kwargs)


class _Command:
    def __init__(self, func):
        self._func = func

    def __get__(self, instance, owner):
        print(instance)
        return _CommandMethod(instance, owner, self._func)


T = TypeVar("T")


def command(func: T) -> T:
    return _Command(func)
