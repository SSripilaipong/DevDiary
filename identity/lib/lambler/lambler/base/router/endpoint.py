from abc import ABC

from lambler.base.event import LamblerEvent


class Endpoint(ABC):
    def can_accept(self, event: LamblerEvent) -> bool:
        pass
