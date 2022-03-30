from abc import ABC, abstractmethod
from typing import Dict, Any

from lambler.base.response import LamblerResponse


class Handler(ABC):

    @abstractmethod
    def handle(self) -> LamblerResponse:
        pass


class PatternMatcher(ABC):

    @abstractmethod
    def match(self, event: Dict, context: Any) -> Handler:
        pass
