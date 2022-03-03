from abc import ABC, abstractmethod
from typing import Dict, Any


class ServiceEvent(ABC):

    @classmethod
    @abstractmethod
    def match(cls, raw_event: Dict) -> bool:
        pass

    @classmethod
    @abstractmethod
    def from_raw_event(cls, raw_event: Dict) -> 'ServiceEvent':
        pass

    @abstractmethod
    def handle(self) -> Any:
        pass
