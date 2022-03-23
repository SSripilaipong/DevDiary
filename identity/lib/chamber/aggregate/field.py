from typing import Type

from chamber.aggregate import Aggregate
from chamber.aggregate.exception import FieldHasNoGetterException, FieldHasNoSetterException

FIELD_MUST_HAVE_TYPE_MSG = "A field must be annotated with a type."


class Field:
    def __init__(self, alias: str = None, *, getter=False, setter=False, serialize=True):
        assert alias is None or isinstance(alias, str)
        assert isinstance(getter, bool)
        assert isinstance(setter, bool)

        self._alias = alias
        self._has_getter = getter
        self._has_setter = setter

    def __set_name__(self, owner: Type[Aggregate], name: str):
        try:
            annotations = owner.__annotations__
        except AttributeError:
            raise TypeError(FIELD_MUST_HAVE_TYPE_MSG)

        self._type = annotations.get(name, None)
        if self._type is None:
            raise TypeError(FIELD_MUST_HAVE_TYPE_MSG)

        if not hasattr(owner, '_Aggregate__chamber_registered_fields'):
            owner._Aggregate__chamber_registered_fields = {}
        owner._Aggregate__chamber_registered_fields[name] = self

        self._name = f'_{name}'

    def __set__(self, instance: Aggregate, value):
        if not isinstance(value, self._type):
            raise TypeError()

        if instance._Aggregate__chamber_field_controller.can_write:
            return setattr(instance, self._name, value)

        if not self._has_setter:
            raise FieldHasNoSetterException()

        setattr(instance, self._name, value)

    def __get__(self, instance: Aggregate, owner: Type[Aggregate]):
        if instance._Aggregate__chamber_field_controller.can_read:
            return getattr(instance, self._name)

        if not self._has_getter:
            raise FieldHasNoGetterException()

        return getattr(instance, self._name)

    @property
    def alias(self) -> str:
        return self._alias
