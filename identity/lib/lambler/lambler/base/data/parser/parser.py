from abc import ABC, abstractmethod

from typing import Dict, Any, Type, TypeVar


T = TypeVar("T", bound="Parser")


class Parser(ABC):
    @classmethod
    @abstractmethod
    def from_type(cls: T, type_: Type) -> T:
        pass

    @abstractmethod
    def parse(self, data: Any) -> Any:
        pass
