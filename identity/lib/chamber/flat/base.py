from abc import abstractmethod

from typing import Callable, Any, TypeVar, Type


class FlatMeta(type):
    def __new__(mcs, name, bases, dct):
        for base in bases:
            getattr(base, "_validate_config", lambda _: ...)(dct)
        if "_validate_config" in dct:
            dct["_validate_config"](dct)
        x = super().__new__(mcs, name, bases, dct)
        return x


T = TypeVar("T", bound='Flat')


class Flat(metaclass=FlatMeta):
    def __init__(self, value: Any, type_: Type):
        self._value = self._validate(value, type_)
        self.__type = type_

    @classmethod
    def _validate(cls, value: Any, type_: Type) -> Any:
        return cls.__flat_ensure_type(value, type_)

    @classmethod
    def __flat_ensure_type(cls, value: Any, type_: Type) -> Any:
        if not isinstance(value, type_):
            raise cls.InvalidTypeException(f"Expect type {type_.__name__} (got {type(value).__name__})")
        return value

    @abstractmethod
    def serialize(self) -> Any:
        pass

    @classmethod
    @abstractmethod
    def deserialize(cls: Type[T], value: Any) -> T:
        pass

    class InvalidTypeException(Exception):
        pass

    class CastingFailedException(Exception):
        pass
