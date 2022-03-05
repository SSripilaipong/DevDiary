from chamber.flat.base import Flat


class StringFlat(Flat):
    MIN_LENGTH: int = None
    MAX_LENGTH: int = None
    VALID_CHARACTERS: str = None

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
        if cls.VALID_CHARACTERS is not None and set(value) - set(cls.VALID_CHARACTERS) != set():
            raise cls.ContainsInvalidCharactersException(f"All characters must be a member of valid characters. "
                                                         f"(got {value})")
        return value

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
