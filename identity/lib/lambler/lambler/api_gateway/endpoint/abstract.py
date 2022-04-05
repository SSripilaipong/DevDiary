from abc import abstractmethod

from lambler.base.handler import PatternMatcher


class HTTPPathPattern(PatternMatcher):
    @property
    @abstractmethod
    def path_length(self) -> int:
        pass
