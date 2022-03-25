from contextlib import contextmanager

from typing import Dict, Set, TYPE_CHECKING

from chamber.data.access_controller import AccessController


class DataModel:
    __chamber_registered_fields: Dict

    def __init__(self, **kwargs):
        provided_keys = set(kwargs)
        required_keys = self.__chamber_get_keys_from_annotations()
        _validate_initial_values(provided_keys, required_keys)
        self.__chamber_access_controller = AccessController()
        self.__chamber_assign_fields(kwargs)

    def to_dict(self) -> Dict:
        result = {}
        with self._DataModel__chamber_request_read_access():
            for name, field in self.__chamber_registered_fields.items():
                if not field.should_serialize:
                    continue

                value = getattr(self, name)
                if hasattr(value, 'serialize'):
                    value = value.serialize()
                result[field.alias or name] = value
        return result

    def __chamber_assign_fields(self, data: Dict):
        with self.__chamber_request_read_write_access():
            for key, value in data.items():
                setattr(self, key, value)

    def __chamber_get_keys_from_annotations(self) -> Set[str]:
        from chamber.data.field import Field
        return set(name for name in getattr(self, '__annotations__', {}).keys()
                   if isinstance(vars(self.__class__).get(name, None), Field))

    @contextmanager
    def __chamber_request_read_access(self):
        self.__chamber_access_controller.allow_read()
        yield
        self.__chamber_access_controller.prevent_read()

    @contextmanager
    def __chamber_request_read_write_access(self):
        self.__chamber_access_controller.allow_read_write()
        yield
        self.__chamber_access_controller.prevent_read_write()

    def __chamber_can_read(self) -> bool:
        return self.__chamber_access_controller.can_read()

    def __chamber_can_write(self) -> bool:
        return self.__chamber_access_controller.can_write()

    if TYPE_CHECKING:
        def _DataModel__chamber_can_write(self) -> bool:
            pass

        def _DataModel__chamber_can_read(self) -> bool:
            pass

        @contextmanager
        def _DataModel__chamber_request_read_access(self):
            pass

        @contextmanager
        def _DataModel__chamber_request_read_write_access(self):
            pass


def _validate_initial_values(provided_keys, required_keys):
    exceeded_keys = provided_keys - required_keys
    lacked_keys = required_keys - provided_keys

    if exceeded_keys != set():
        message = "Unknown fields named: " + ', '.join(list(exceeded_keys))
        raise AttributeError(message)

    if lacked_keys != set():
        message = "Required fields not provided: " + ', '.join(list(lacked_keys))
        raise AttributeError(message)
