from typing import Any, List, Dict, TypeVar, Type

from chamber.aggregate.field_controller import FieldController
from chamber.aggregate.version import AggregateVersion
from chamber.aggregate.version_increase import AggregateVersionIncrease
from chamber.message import Message


T = TypeVar('T', bound='Aggregate')


class Aggregate:
    __chamber_registered_fields: Dict
    __chamber_registered_alias_fields: Dict
    _Aggregate__chamber_field_controller: FieldController

    def __init__(self, *, _aggregate_version: AggregateVersion = None, _outbox: List[Message] = None, **kwargs):
        self.__chamber_aggregate_version = _aggregate_version or AggregateVersion.create(0)
        self.__chamber_outbox = _outbox or []

        self.__chamber_field_controller = FieldController()

        self.__chamber_assign_fields(kwargs)

    @classmethod
    def from_dict(cls: Type[T], data: Dict) -> T:
        params = {}

        for key, value in data.items():
            field = cls.__chamber_registered_alias_fields.get(key, None)
            if field is not None:
                name = field.name
                type_ = field.type_
            else:
                field = cls.__chamber_registered_fields.get(key, None)
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

    def to_dict(self) -> Dict:
        result = {}
        with self.__chamber_field_controller.allow_read():
            for name, field in self.__chamber_registered_fields.items():
                if not field.should_serialize:
                    continue

                value = getattr(self, name)
                if hasattr(value, 'serialize'):
                    value = value.serialize()
                result[field.alias or name] = value
        return result

    def __chamber_assign_fields(self, data: Dict[str, Any]):
        from chamber.aggregate import Field
        provided_keys = set(data)
        required_keys = set(name for name in getattr(self, '__annotations__', {}).keys()
                            if isinstance(vars(self.__class__).get(name, None), Field))
        _validate_initial_values(provided_keys, required_keys)

        with self.__chamber_field_controller.allow_read_write():
            for key, value in data.items():
                setattr(self, key, value)

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


def _is_integer(number: Any) -> bool:
    try:
        return number == int(number)
    except ValueError:
        return False


def _validate_initial_values(provided_keys, required_keys):
    exceeded_keys = provided_keys - required_keys
    lacked_keys = required_keys - provided_keys

    if exceeded_keys != set():
        message = "Unknown fields named: " + ', '.join(list(exceeded_keys))
        raise AttributeError(message)

    if lacked_keys != set():
        message = "Required fields not provided: " + ', '.join(list(lacked_keys))
        raise AttributeError(message)
