from abc import ABC, abstractmethod

from lambler.base.event import LamblerEvent


class Endpoint(ABC):
    @abstractmethod
    def can_accept(self, event: LamblerEvent) -> bool:
        pass
