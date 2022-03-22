from typing import Type

from chamber.aggregate import Aggregate


class Field:
    def __set_name__(self, owner: Type[Aggregate], name: str):
        self._type = owner.__annotations__.get(name, None)
        if self._type is None:
            return  # TODO: handle this

    def __set__(self, instance: Aggregate, value):
        if not isinstance(value, self._type):
            raise TypeError()
