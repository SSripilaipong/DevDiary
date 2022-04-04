from typing import Type, Dict, Any

from abc import ABC, abstractmethod


class Marker(ABC):
    @abstractmethod
    def register_type(self, type_: Type):
        pass

    @abstractmethod
    def extract_param(self, data: Dict) -> Any:
        pass
