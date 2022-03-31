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
            if param.annotation is Signature.empty:
                raise TypeError("Usecase's parameters should be type-annotated.")
            param_list.append((name, param))

        return ParameterValidator(param_list)
