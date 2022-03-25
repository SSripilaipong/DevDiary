from typing import List, Dict, TypeVar, Type

from chamber.aggregate.version import AggregateVersion
from chamber.aggregate.version_increase import AggregateVersionIncrease
from chamber.data.model import DataModel
from chamber.message import Message


T = TypeVar('T', bound='Aggregate')


class Aggregate(DataModel):
    def __init__(self, *, _aggregate_version: AggregateVersion = None, _outbox: List[Message] = None, **kwargs):
        super().__init__(**kwargs)
        self.__chamber_aggregate_version = _aggregate_version or AggregateVersion(0)
        self.__chamber_outbox = _outbox or []

    @classmethod
    def from_dict(cls: Type[T], data: Dict) -> T:
        params = {}

        for key, value in data.items():
            field = cls._DataModel__chamber_registered_alias_fields.get(key, None)
            if field is not None:
                name = field.name
                type_ = field.type_
            else:
                field = cls._DataModel__chamber_registered_fields.get(key, None)
                if field is None:
                    raise AttributeError(f'Invalid field name: {key}')

                name = key
                type_ = field.type_

            if not isinstance(value, type_):
                if hasattr(type_, 'deserialize'):
                    value = type_.deserialize(value)
                else:
                    raise TypeError(f'Expect type {type_.__name__} got: {value.__class__.__name__}')

            params[name] = value
        return cls(**params)

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
