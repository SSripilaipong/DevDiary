from typing import Any, List, Dict

from chamber.aggregate.field_controller import FieldController
from chamber.aggregate.version import AggregateVersion
from chamber.aggregate.version_increase import AggregateVersionIncrease
from chamber.message import Message


class Aggregate:
    __chamber_registered_fields: Dict

    def __init__(self, _aggregate_version: AggregateVersion = None, _outbox: List[Message] = None, **kwargs):
        self._aggregate_version = _aggregate_version or AggregateVersion.create(0)
        self._outbox = _outbox or []

        self._field_controller = FieldController()

        self._assign_fields(kwargs)

    def to_dict(self) -> Dict:
        result = {}
        with self._field_controller.allow_read():
            for name in self.__chamber_registered_fields.keys():
                result[name] = getattr(self, name)
        return result

    def _assign_fields(self, data: Dict[str, Any]):
        provided_keys = set(data)
        required_keys = set(getattr(self, '__annotations__', {}).keys())
        _validate_initial_values(provided_keys, required_keys)

        with self._field_controller.allow_read_write():
            for key, value in data.items():
                setattr(self, key, value)

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


def _validate_initial_values(provided_keys, required_keys):
    exceeded_keys = provided_keys - required_keys
    lacked_keys = required_keys - provided_keys

    if exceeded_keys != set():
        message = "Unknown fields named: " + ', '.join(list(exceeded_keys))
        raise AttributeError(message)

    if lacked_keys != set():
        message = "Required fields not provided: " + ', '.join(list(lacked_keys))
        raise AttributeError(message)
