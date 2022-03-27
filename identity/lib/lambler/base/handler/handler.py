from abc import ABC, abstractmethod
from typing import Dict, Any


class HandlerMatcher(ABC):

    @classmethod
    @abstractmethod
    def match(cls, raw_event: Dict) -> bool:
        pass

    @abstractmethod
    def handle(self, raw_event: Dict) -> Any:
        pass
