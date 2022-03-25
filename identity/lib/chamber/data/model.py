from contextlib import contextmanager

from typing import Dict, Set, TYPE_CHECKING, Type, TypeVar

from chamber.data.access_controller import AccessController


T = TypeVar('T', bound='DataModel')


class DataModel:
    __chamber_registered_fields: Dict
    __chamber_registered_alias_fields: Dict

    def __init__(self, **kwargs):
        provided_keys = set(kwargs)
        required_keys = self.__chamber_get_keys_from_annotations()
        _validate_initial_values(provided_keys, required_keys)
        self.__chamber_access_controller = AccessController()
        self.__chamber_assign_fields(kwargs)

    def to_dict(self) -> Dict:
        result = {}
        with self.__chamber_request_read_access():
            for name, field in self.__chamber_registered_fields.items():
                if not field.should_serialize:
                    continue

                value = getattr(self, name)
                if hasattr(value, 'serialize'):
                    value = value.serialize()
                result[field.alias or name] = value
        return result

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
