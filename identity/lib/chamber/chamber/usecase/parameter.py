from collections import deque

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

    def validate_parameter(self, *args, **kwargs):
        args = deque(args)
        for name, param in self._parameters:
            annotation = param.annotation
            default = param.default
            if param.kind in [Parameter.POSITIONAL_OR_KEYWORD, Parameter.POSITIONAL_ONLY]:
                if len(args) > 0:
                    value = args.popleft()
                elif name in kwargs:
                    value = kwargs.pop(name)
                elif default is not Signature.empty:
                    raise NotImplementedError()
                else:
                    raise TypeError(f"Usecase's parameter {name} is missing.")

                if not isinstance(value, annotation):
                    raise TypeError(f"Usecase's parameter {name} should be {annotation.__name__}")
            else:
                raise NotImplementedError()
