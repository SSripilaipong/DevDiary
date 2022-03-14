from typing import Any, List

from lib.chamber.aggregate.version import AggregateVersion
from lib.chamber.aggregate.version_increase import AggregateVersionIncrease
from lib.chamber.message import Message


class Aggregate:
    def __init__(self, aggregate_version: AggregateVersion, outbox: List[Message] = None):
        self._aggregate_version = aggregate_version
        self._outbox = outbox or []

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
