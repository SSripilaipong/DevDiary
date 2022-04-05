from lambler.api_gateway.endpoint import HTTPPathPattern


class PathPatternSortWrapper:
    def __init__(self, pattern: HTTPPathPattern):
        self._pattern = pattern

    def __eq__(self, other):
        assert isinstance(other, PathPatternSortWrapper)
        return self._pattern.path_length == other._pattern.path_length

    def __lt__(self, other):
        assert isinstance(other, PathPatternSortWrapper)
        return self._pattern.path_length < other._pattern.path_length

    def __le__(self, other):
        assert isinstance(other, PathPatternSortWrapper)
        return self._pattern.path_length <= other._pattern.path_length

    @property
    def pattern(self) -> HTTPPathPattern:
        return self._pattern