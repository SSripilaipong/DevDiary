from typing import List

from chamber.aggregate.version import AggregateVersion
from chamber.aggregate.version_increase import AggregateVersionIncrease
from chamber.data.model import DataModel
from chamber.message import Message


class Aggregate(DataModel):
    def __init__(self, *, _aggregate_version: AggregateVersion = None, _outbox: List[Message] = None, **kwargs):
        super().__init__(**kwargs)
        self.__chamber_aggregate_version = _aggregate_version or AggregateVersion(0)
        self.__chamber_outbox = _outbox or []

    def _append_message(self, message: Message):
        self.__chamber_outbox.append(message)

    def get_aggregate_outbox_messages(self) -> List[Message]:
        return list(self.__chamber_outbox)

    def clear_aggregate_outbox_messages(self):
        self.__chamber_outbox = []

    @property
    def aggregate_version(self) -> AggregateVersion:
        return self.__chamber_aggregate_version

    def increase_aggregate_version_by(self, increase: AggregateVersionIncrease):
        self.__chamber_aggregate_version = increase.apply_to(self.__chamber_aggregate_version)
