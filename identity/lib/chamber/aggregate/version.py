from chamber.aggregate.exception import InvalidAggregateVersionException
from chamber.flat.integer import IntegerFlat


class AggregateVersion(IntegerFlat):
    MIN_VALUE = 0

    TooLowException = InvalidAggregateVersionException
    InvalidTypeException = InvalidAggregateVersionException
