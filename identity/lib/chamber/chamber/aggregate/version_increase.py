from chamber.aggregate.exception import InvalidAggregateVersionException
from chamber.aggregate.version import AggregateVersion
from chamber.flat.integer import IntegerFlat


class AggregateVersionIncrease(IntegerFlat):
    MIN_VALUE = 0

    TooLowException = InvalidAggregateVersionException
    InvalidTypeException = InvalidAggregateVersionException

    def apply_to(self, version: AggregateVersion) -> AggregateVersion:
        return AggregateVersion(version.int() + self._value)
