import datetime
from abc import ABC, abstractmethod


class Clock(ABC):
    @abstractmethod
    def get_current_timestamp(self) -> int:
        pass


class RealClock(Clock):
    def get_current_timestamp(self) -> int:
        return int(datetime.datetime.now().timestamp())
