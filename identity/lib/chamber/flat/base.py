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
    def __init__(self, value: Any, type_: Type, cast: Callable[[Any], Any] = None):
        self._value = self._validate(value, type_, cast)

    @classmethod
    def as_is(cls: Type[T], value: Any) -> T:
        pass

    @classmethod
    def _validate(cls, value: Any, type_: Type, cast: Callable[[Any], Any]) -> Any:
        return cls.__flat_ensure_type(value, type_, cast)

    @classmethod
    def __flat_ensure_type(cls, value: Any, type_: Type, cast: Callable[[Any], Any]) -> Any:
        if not isinstance(value, type_):
            if cast is None:
                raise cls.InvalidTypeException(f"Expect type {type_.__name__} (got {type(value).__name__})")
            try:
                value = cast(value)
            except Exception:
                raise cls.CastingFailedException(f"Casting with the provided cast function raises error.")
            if not isinstance(value, type_):
                raise cls.CastingFailedException(f"Casting doesn't return with type {type_.__name__} "
                                                 f"(got {type(value).__name__}).")
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
