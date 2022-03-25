from typing import Dict, Type, TypeVar

from chamber.data.exception import DeserializationFailedException
from chamber.data.model import DataModel


T = TypeVar("T", bound="Message")


class Message(DataModel):
    def to_dict(self) -> Dict:
        return {
            'name': self.__class__.__name__,
            'body': super().to_dict(),
        }

    @classmethod
    def from_dict(cls: Type[T], data: Dict) -> T:
        name = data.get('name', None)
        if name != cls.__name__:
            raise DeserializationFailedException(f"Cannot deserialize data with name {name}")

        return super().from_dict(data['body'])
