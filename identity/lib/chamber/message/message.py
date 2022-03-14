from abc import abstractmethod, ABC
from typing import Dict, Type, TypeVar

M = TypeVar('M', bound='Message')


class Message(ABC):
    def to_dict(self) -> Dict:
        return {
            'name': self.__class__.__name__,
            'body': self._body_to_dict(),
        }

    @classmethod
    def from_dict(cls: Type[M], obj: Dict) -> M:
        return cls._body_from_dict(obj['body'])

    @abstractmethod
    def _body_to_dict(self) -> Dict:
        pass

    @classmethod
    @abstractmethod
    def _body_from_dict(cls: Type[M], obj: Dict) -> M:
        pass
