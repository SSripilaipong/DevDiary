from typing import Dict, Type, TypeVar

from chamber.flat.base import Flat
from chamber.flat.integer.validate_config import _validate_min_value_config, _validate_max_value_config

F = TypeVar("F", bound="IntegerFlat")


class IntegerFlat(Flat):
    MIN_VALUE: int = None
    MAX_VALUE: int = None

    def __init__(self, value: int):
        if value is None:
            self._value = None
        else:
            self._value = self._validate(value)

    @classmethod
    def as_is(cls: Type[F], value: int) -> F:
        flat = cls(None)
        flat._value = value
        return flat

    @classmethod
    def _validate(cls, value: int) -> int:
        value = cls._flat_ensure_integer(value)
        cls._flat_validate_range(value)
        return value

    @classmethod
    def _flat_ensure_integer(cls, value) -> int:
        if not isinstance(value, int):
            if cls.CAST is None:
                raise cls.InvalidTypeException(f"Only integer value is accepted unless CAST function is specified.")
            try:
                value = cls.CAST(value)
            except Exception:
                raise cls.CastingFailedException(f"Casting with the provided CAST function failed.")
            if not isinstance(value, int):
                raise cls.CastingFailedException(f"CAST function should return integer value.")
        return value

    @classmethod
    def _flat_validate_range(cls, value: int):
        if value < cls.MIN_VALUE:
            raise cls.TooLowException(f"Value must be at least {cls.MIN_VALUE} (got {value}).")
        if cls.MAX_VALUE < value:
            raise cls.TooHighException(f"Value must be at most {cls.MAX_VALUE} (got {value}).")

    def _validate_config(dct: Dict):
        validators = {
            "MIN_VALUE": _validate_min_value_config,
            "MAX_VALUE": _validate_max_value_config,
        }

        for field_name, validator in validators.items():
            dct[field_name] = validator(dct.get(field_name, None))

    def serialize(self) -> int:
        return self.int()

    def int(self) -> int:
        return int(self._value)

    @classmethod
    def deserialize(cls: Type[F], value: int) -> F:
        return cls(value)

    def __int__(self) -> int:
        return self.int()

    def __eq__(self, other) -> bool:
        if type(self) != type(other):
            return False
        assert isinstance(other, IntegerFlat)
        return self._value == other._value

    def __hash__(self):
        return self._value.__hash__()

    class TooLowException(Exception):
        pass

    class TooHighException(Exception):
        pass
