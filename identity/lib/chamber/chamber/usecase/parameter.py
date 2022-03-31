import inspect
from inspect import Parameter, Signature

from typing import Callable, List, Tuple


class ParameterValidator:
    def __init__(self, parameters: List[Tuple[str, Parameter]]):
        self._parameters = parameters

    @classmethod
    def from_function(cls, func: Callable) -> 'ParameterValidator':
        params = inspect.signature(func).parameters
        param_list = []
        for name, param in params.items():
            annotation = param.annotation
            if annotation is Signature.empty:
                raise TypeError("Usecase's parameters should be type-annotated.")
            elif not isinstance(annotation, type):
                raise TypeError("Usecase's parameters should be annotated with a type.")
            param_list.append((name, param))

        return ParameterValidator(param_list)
