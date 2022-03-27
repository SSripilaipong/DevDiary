from typing import Type

from chamber.data.exception import FieldHasNoSetterException, FieldHasNoGetterException
from chamber.data.model import DataModel

FIELD_MUST_HAVE_TYPE_MSG = "A field must be annotated with a type."


class Field:
    def __init__(self, alias: str = None, *, getter=False, setter=False, serialize=True):
        assert alias is None or isinstance(alias, str)
        assert isinstance(getter, bool)
        assert isinstance(setter, bool)

        self._alias = alias
        self._has_getter = getter
        self._has_setter = setter
        self._should_serialize = serialize

    def __set_name__(self, owner: Type[DataModel], name: str):
        assert issubclass(owner, DataModel)

        try:
            annotations = owner.__annotations__
        except AttributeError:
            raise TypeError(FIELD_MUST_HAVE_TYPE_MSG)

        self._type = annotations.get(name, None)
        if self._type is None:
            raise TypeError(FIELD_MUST_HAVE_TYPE_MSG)

        if not hasattr(owner, '_DataModel__chamber_registered_fields'):
            owner._DataModel__chamber_registered_fields = {}
        owner._DataModel__chamber_registered_fields[name] = self

        if not hasattr(owner, f'_DataModel__chamber_registered_alias_fields'):
            owner._DataModel__chamber_registered_alias_fields = {}
        owner._DataModel__chamber_registered_alias_fields[self.alias] = self

        self._value_name = f'_{name}'
        self._name = name

    def __set__(self, instance: DataModel, value):
        if not isinstance(value, self._type):
            raise TypeError()

        if instance._DataModel__chamber_can_write():
            return setattr(instance, self._value_name, value)

        if not self._has_setter:
            raise FieldHasNoSetterException()

        setattr(instance, self._value_name, value)

    def __get__(self, instance: DataModel, owner: Type[DataModel]):
        if instance._DataModel__chamber_can_read():
            return getattr(instance, self._value_name)

        if not self._has_getter:
            raise FieldHasNoGetterException()

        return getattr(instance, self._value_name)

    @property
    def alias(self) -> str:
        return self._alias

    @property
    def type_(self) -> Type:
        return self._type

    @property
    def name(self) -> str:
        return self._name

    @property
    def should_serialize(self) -> bool:
        return self._should_serialize
