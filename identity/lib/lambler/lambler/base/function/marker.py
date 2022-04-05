from typing import Type, Any

from abc import ABC, abstractmethod

from lambler.base.function.input import FunctionInputSourceCollection


class Marker(ABC):
    @abstractmethod
    def register_type(self, type_: Type):
        pass

    @abstractmethod
    def extract_param(self, data: FunctionInputSourceCollection) -> Any:
        pass
