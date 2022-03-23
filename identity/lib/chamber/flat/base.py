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
    CAST: Callable[[Any], str] = None

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
