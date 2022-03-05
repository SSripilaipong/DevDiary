from typing import Callable, Any


class FlatMeta(type):
    def __new__(mcs, name, bases, dct):
        for base in bases:
            getattr(base, "_validate_config", lambda _: ...)(dct)
        if "_validate_config" in dct:
            dct["_validate_config"](dct)
        x = super().__new__(mcs, name, bases, dct)
        return x


class Flat(metaclass=FlatMeta):
    CAST: Callable[[Any], str] = None

    class InvalidTypeException(Exception):
        pass

    class CastingFailedException(Exception):
        pass
