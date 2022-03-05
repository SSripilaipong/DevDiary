from typing import Dict, Union, Set, List

from chamber.flat.base import Flat


class StringFlat(Flat):
    MIN_LENGTH: int = None
    MAX_LENGTH: int = None
    VALID_CHARACTERS: Union[str, Set[str]] = None
    REQUIRED_CHARACTER_SETS: Union[str, List[str], List[Set[str]]] = None

    def __init__(self, value: str):
        self._value = self._validate(value)

    @classmethod
    def _validate(cls, value: str) -> str:
        if not isinstance(value, str):
            if cls.CAST is None:
                raise cls.InvalidTypeException(f"Only string value is accepted unless CAST function is specified "
                                               f"(got {value!r}).")
            try:
                value = cls.CAST(value)
            except Exception:
                raise cls.CastingFailedException(f"Casting with the provided CAST function failed (got {value!r}).")
            if not isinstance(value, str):
                raise cls.CastingFailedException(f"CAST function should return string value (got {value!r}).")

        if cls.MIN_LENGTH is not None and len(value) < cls.MIN_LENGTH:
            raise cls.TooShortException(f"Value must be at least {cls.MIN_LENGTH} length (got {len(value)}).")
        elif cls.MAX_LENGTH is not None and cls.MAX_LENGTH < len(value):
            raise cls.TooLongException(f"Value must be at most {cls.MIN_LENGTH} length (got {len(value)}).")

        chars = set(value)
        if cls.VALID_CHARACTERS is not None and chars - cls.VALID_CHARACTERS != set():
            raise cls.ContainsInvalidCharactersException(f"All characters must be a member of valid characters. "
                                                         f"(got {value})")
        if cls.REQUIRED_CHARACTER_SETS is not None:
            for char_set in cls.REQUIRED_CHARACTER_SETS:  # type: Set[str]
                if chars & char_set == set():
                    required = [''.join(_char_set) for _char_set in cls.REQUIRED_CHARACTER_SETS]
                    raise cls.RequiredCharactersMissingException(f'Required characters are {required!r} '
                                                                 f'(got {value}).')
        return value

    def _validate_config(dct: Dict):
        min_length = dct.get("MIN_LENGTH", None)
        if min_length is not None:
            assert isinstance(min_length, int)

        max_length = dct.get("MAX_LENGTH", None)
        if max_length is not None:
            assert isinstance(max_length, int)

        chars = dct.get("VALID_CHARACTERS", None)
        if chars is not None:
            assert isinstance(chars, (str, set, list, tuple))
            dct["VALID_CHARACTERS"] = set(dct["VALID_CHARACTERS"])

        char_sets = dct.get("REQUIRED_CHARACTER_SETS", None)
        if char_sets is not None:
            if isinstance(char_sets, str):
                dct["REQUIRED_CHARACTER_SETS"] = set(char_sets)
            else:
                assert isinstance(char_sets, (list, tuple))
                dct["REQUIRED_CHARACTER_SETS"] = [set(_set) for _set in char_sets]

    def str(self) -> str:
        return self._value

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
