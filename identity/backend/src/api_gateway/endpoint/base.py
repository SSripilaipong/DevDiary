from abc import abstractmethod, ABC
from typing import Any, Dict


class Endpoint(ABC):
    @abstractmethod
    def process(self, headers: Dict[str, str], query: Dict[str, Any], body: str):
        pass
