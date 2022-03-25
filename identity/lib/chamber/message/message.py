from typing import Dict, Type, TypeVar

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
        return super().from_dict(data['body'])
