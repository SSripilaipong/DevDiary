from typing import TypeVar, Type

from chamber.aggregate import Aggregate


class _QueryMethod:
    def __init__(self, instance: Aggregate, owner: Type, func):
        self._instance = instance
        self._owner = owner
        self._func = func

    def __call__(self, *args, **kwargs):
        from chamber.data.model import DataModel
        if issubclass(self._owner, DataModel):
            with self._instance._DataModel__chamber_request_read_access():
                return self._func(self._instance, *args, **kwargs)
        with self._instance._Aggregate__chamber_field_controller.allow_read():
            return self._func(self._instance, *args, **kwargs)


class _Query:
    def __init__(self, func):
        self._func = func

    def __get__(self, instance, owner):
        print(instance)
        return _QueryMethod(instance, owner, self._func)


T = TypeVar("T")


def query(func: T) -> T:
    return _Query(func)
