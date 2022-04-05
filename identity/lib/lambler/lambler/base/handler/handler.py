from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from lambler.base.response import LamblerResponse


class Handler(ABC):

    @abstractmethod
    def handle(self) -> LamblerResponse:
        pass


class PatternMatcher(ABC):

    @abstractmethod
    def match(self, event: Any, context: Any) -> Optional[Handler]:
        pass
