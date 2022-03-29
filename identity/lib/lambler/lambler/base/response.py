from typing import Dict

from abc import ABC, abstractmethod


class LamblerResponse(ABC):
    @abstractmethod
    def to_dict(self) -> Dict:
        pass
