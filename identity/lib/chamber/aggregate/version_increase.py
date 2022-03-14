from typing import Any

from lib.chamber.aggregate.exception import InvalidAggregateVersionException
from lib.chamber.aggregate.version import AggregateVersion


class AggregateVersionIncrease:
    def __init__(self, version_increase: int):
        self._version_increase = version_increase

    @classmethod
    def create(cls, version_increase: int) -> 'AggregateVersionIncrease':
        """
        :raises:
            InvalidAggregateVersionException: increase
        """
        if not _is_integer(version_increase):
            raise InvalidAggregateVersionException(f"Aggregate version increase must be an integer "
                                                   f"(got: {repr(version_increase)})")
        if version_increase < 0:
            raise InvalidAggregateVersionException(f"Aggregate version increase must be not be "
                                                   f"(got: {repr(version_increase)})")
        return cls(version_increase)

    def int(self) -> int:
        return self._version_increase

    def apply_to(self, version: AggregateVersion) -> AggregateVersion:
        return AggregateVersion.create(version.int() + self._version_increase)


def _is_integer(number: Any) -> bool:
    try:
        return number == int(number)
    except ValueError:
        return False
