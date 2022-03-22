from typing import Any, List

from chamber.aggregate.version import AggregateVersion
from chamber.aggregate.version_increase import AggregateVersionIncrease
from chamber.message import Message


class Aggregate:
    def __init__(self, _aggregate_version: AggregateVersion = None, _outbox: List[Message] = None, **kwargs):
        self._aggregate_version = _aggregate_version or AggregateVersion.create(0)
        self._outbox = _outbox or []

        annotations = self.__annotations__
        for key, value in kwargs.items():
            type_ = annotations.get(key, None)

            if not isinstance(value, type_):
                raise TypeError()

    def _append_message(self, message: Message):
        self._outbox.append(message)

    def get_aggregate_outbox_messages(self) -> List[Message]:
        return list(self._outbox)

    def clear_aggregate_outbox_messages(self):
        self._outbox = []

    @property
    def aggregate_version(self) -> AggregateVersion:
        return self._aggregate_version

    def increase_aggregate_version_by(self, increase: AggregateVersionIncrease):
        self._aggregate_version = increase.apply_to(self._aggregate_version)


def _is_integer(number: Any) -> bool:
    try:
        return number == int(number)
    except ValueError:
        return False
