from typing import Any

from chamber.aggregate.exception import InvalidAggregateVersionException


class AggregateVersion:
    def __init__(self, version_number: int):
        self._version_number = version_number

    @classmethod
    def create(cls, version_number: int) -> 'AggregateVersion':
        """
        :raises:
            InvalidAggregateVersionException: increase
        """
        if not _is_integer(version_number):
            raise InvalidAggregateVersionException(f"Aggregate version number must be an integer "
                                                   f"(got: {repr(version_number)})")
        if version_number < 0:
            raise InvalidAggregateVersionException(f"Aggregate version number must be not be negative "
                                                   f"(got: {repr(version_number)})")
        return cls(version_number)

    def int(self) -> int:
        return self._version_number

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        assert isinstance(other, AggregateVersion)
        return self._version_number == other._version_number

    def __lt__(self, other):
        if type(self) != type(other):
            return False
        assert isinstance(other, AggregateVersion)
        return self._version_number < other._version_number


def _is_integer(number: Any) -> bool:
    try:
        return number == int(number)
    except ValueError:
        return False
