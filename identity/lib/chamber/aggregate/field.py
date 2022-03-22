from typing import Type

from chamber.aggregate import Aggregate

FIELD_MUST_HAVE_TYPE_MSG = "A field must be annotated with a type."


class Field:
    def __set_name__(self, owner: Type[Aggregate], name: str):
        try:
            annotations = owner.__annotations__
        except AttributeError:
            raise TypeError(FIELD_MUST_HAVE_TYPE_MSG)

        self._type = annotations.get(name, None)
        if self._type is None:
            raise TypeError(FIELD_MUST_HAVE_TYPE_MSG)

    def __set__(self, instance: Aggregate, value):
        if not isinstance(value, self._type):
            raise TypeError()
