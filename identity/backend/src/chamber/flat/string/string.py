import re
from typing import Dict, Union, Set, List, Type, TypeVar

from chamber.flat.base import Flat
from chamber.flat.string.validate_config import _validate_min_length_config, _validate_max_length_config, \
    _validate_valid_characters_config, _validate_required_character_config, _validate_pattern_config

F = TypeVar("F", bound="StringFlat")


class StringFlat(Flat):
    MIN_LENGTH: int = None
    MAX_LENGTH: int = None
    VALID_CHARACTERS: Union[str, Set[str]] = None
    REQUIRED_CHARACTER_SETS: Union[str, List[str], List[Set[str]]] = None
    PATTERN: Union[str, re.Pattern] = None

    def __init__(self, value: str):
        if value is None:
            self._value = None
        else:
            self._value = self._validate(value)

    @classmethod
    def as_is(cls: Type[F], value: str) -> F:
        flat = cls(None)
        flat._value = value
        return flat

    @classmethod
    def _validate(cls, value: str) -> str:
        value = cls._flat_ensure_string(value)
        cls._flat_validate_length(value)
        cls._flat_validate_valid_characters(value)
        cls._flat_validate_required_characters(value)
        cls._flat_validate_pattern(value)
        return value

    @classmethod
    def _flat_ensure_string(cls, value) -> str:
        if not isinstance(value, str):
            if cls.CAST is None:
                raise cls.InvalidTypeException(f"Only string value is accepted unless CAST function is specified.")
            try:
                value = cls.CAST(value)
            except Exception:
                raise cls.CastingFailedException(f"Casting with the provided CAST function failed.")
            if not isinstance(value, str):
                raise cls.CastingFailedException(f"CAST function should return string value.")
        return value

    @classmethod
    def _flat_validate_length(cls, value: str):
        if len(value) < cls.MIN_LENGTH:
            raise cls.TooShortException(f"Value must be at least {cls.MIN_LENGTH} length (got {len(value)}).")
        if cls.MAX_LENGTH < len(value):
            raise cls.TooLongException(f"Value must be at most {cls.MAX_LENGTH} length (got {len(value)}).")

    @classmethod
    def _flat_validate_valid_characters(cls, value: str):
        if cls.VALID_CHARACTERS != set() and set(value) - cls.VALID_CHARACTERS != set():
            raise cls.ContainsInvalidCharactersException(f"All characters must be a member of valid characters.")

    @classmethod
    def _flat_validate_required_characters(cls, value: str):
        for char_set in cls.REQUIRED_CHARACTER_SETS:  # type: Set[str]
            if set(value) & char_set == set():
                required = [''.join(_char_set) for _char_set in cls.REQUIRED_CHARACTER_SETS]
                raise cls.RequiredCharactersMissingException(f'Required characters are {required!r}.')

    @classmethod
    def _flat_validate_pattern(cls, value: str):
        if cls.PATTERN is not None:
            pattern: re.Pattern = cls.PATTERN
            if not pattern.match(value):
                raise cls.PatternNotMatchedException('Value must match with PATTERN.')

    def _validate_config(dct: Dict):
        validators = {
            "MIN_LENGTH": _validate_min_length_config,
            "MAX_LENGTH": _validate_max_length_config,
            "VALID_CHARACTERS": _validate_valid_characters_config,
            "REQUIRED_CHARACTER_SETS": _validate_required_character_config,
            "PATTERN": _validate_pattern_config,
        }

        for field_name, validator in validators.items():
            dct[field_name] = validator(dct.get(field_name, None))

    def str(self) -> str:
        return str(self._value)

    def __str__(self) -> str:
        return self.str()

    def __eq__(self, other) -> bool:
        if type(self) != type(other):
            return False
        assert isinstance(other, StringFlat)
        return self._value == other._value

    def __hash__(self):
        return self._value.__hash__()

    class TooShortException(Exception):
        pass

    class TooLongException(Exception):
        pass

    class ContainsInvalidCharactersException(Exception):
        pass

    class RequiredCharactersMissingException(Exception):
        pass

    class PatternNotMatchedException(Exception):
        pass
