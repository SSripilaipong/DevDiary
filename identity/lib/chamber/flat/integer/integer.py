from typing import Dict, Type, TypeVar, Callable, Any, TYPE_CHECKING

from chamber.flat.base import Flat
from chamber.flat.integer.validate_config import _validate_min_value_config, _validate_max_value_config

F = TypeVar("F", bound="IntegerFlat")


class IntegerFlat(Flat):
    CAST: Callable[[Any], int] = None
    MIN_VALUE: int = None
    MAX_VALUE: int = None

    def __init__(self, value: int, _as_is=False):
        super().__init__(value, type_=int, cast=self.CAST, _as_is=_as_is)

    @classmethod
    def _validate(cls, value: int, *args, **kwargs) -> int:
        value = super()._validate(value, *args, **kwargs)
        cls.__flat_validate_range(value)
        return value

    @classmethod
    def __flat_validate_range(cls, value: int):
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

    def __lt__(self, other):
        return self._value < other._value

    def __hash__(self):
        return self._value.__hash__()

    class TooLowException(Exception):
        pass

    class TooHighException(Exception):
        pass

    if TYPE_CHECKING:
        @classmethod
        def as_is(cls: Type[F], value: int) -> F:
            return cls()

    def int(self) -> int:
        return int(self._value)
