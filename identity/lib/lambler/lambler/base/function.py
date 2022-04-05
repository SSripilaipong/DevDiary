import inspect
from typing import Any, Iterator, Tuple, Callable, Dict

from lambler.base.marker import Marker
from lambler.base.source import FunctionInputSourceCollection


class MarkedFunction:
    def __init__(self, function: Callable, markers: Dict[str, Marker]):
        self._function = function
        self._markers = markers

    @classmethod
    def from_function(cls, function: Callable) -> 'MarkedFunction':
        signature = inspect.signature(function)
        markers = {}
        for name, parameter in signature.parameters.items():
            type_ = parameter.annotation
            marker = parameter.default
            if isinstance(marker, Marker):
                marker.register_type(type_)
                markers[name] = marker
            else:
                raise NotImplementedError()

        return cls(function, markers)

    def execute(self, sources: FunctionInputSourceCollection) -> Any:
        params = {}
        for key, marker in self._iterate_markers():
            params[key] = marker.extract_param(sources)
        return self._function(**params)

    def _iterate_markers(self) -> Iterator[Tuple[str, Marker]]:
        yield from self._markers.items()
