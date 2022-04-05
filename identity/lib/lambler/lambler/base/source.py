from typing import TypeVar, Dict, Type

from abc import ABC


class FunctionInputSource(ABC):
    pass


S = TypeVar("S", bound=FunctionInputSource)


class FunctionInputSourceCollection:
    def __init__(self, sources: Dict[Type[FunctionInputSource], FunctionInputSource] = None):
        self._sources: Dict[Type[FunctionInputSource], FunctionInputSource] = sources or {}

    def of(self, source_type: Type[S]) -> S:
        source = self._sources.get(source_type, None)
        if source is not None:
            return source

        raise NotImplementedError()