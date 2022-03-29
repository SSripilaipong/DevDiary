from abc import ABC, abstractmethod
from typing import Dict, Any


class Handler(ABC):

    @abstractmethod
    def handle(self) -> Any:
        pass


class PatternMatcher(ABC):

    @abstractmethod
    def match(self, event: Dict, context: Any) -> Handler:
        pass
