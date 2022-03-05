from typing import Callable, Any


class FlatMeta(type):
    pass


class Flat(metaclass=FlatMeta):
    CAST: Callable[[Any], str] = None

    class InvalidTypeException(Exception):
        pass

    class CastingFailedException(Exception):
        pass
