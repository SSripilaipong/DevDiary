from collections import deque

import inspect
from inspect import Parameter, Signature

from typing import Callable, List, Tuple, Dict, Any


class ParameterValidator:
    def __init__(self, parameters: List[Tuple[str, Parameter]]):
        self._parameters = parameters

    @classmethod
    def from_function(cls, func: Callable) -> 'ParameterValidator':
        params = inspect.signature(func).parameters
        param_list = []
        for name, param in params.items():
            kind = param.kind
            annotation = param.annotation
            if kind == Parameter.VAR_POSITIONAL:
                raise TypeError(f"Usecase should not have variable-length argument (*{name}).")
            elif kind == Parameter.VAR_KEYWORD:
                raise TypeError(f"Usecase should not have keyword variable-length argument (**{name}).")
            if annotation is Signature.empty:
                raise TypeError("Usecase's parameters should be type-annotated.")
            elif not isinstance(annotation, type):
                raise TypeError("Usecase's parameters should be annotated with a type.")
            param_list.append((name, param))

        return ParameterValidator(param_list)

    def validate_parameter(self, *args, **kwargs):
        _ = self.make_parameter_value_mapping(*args, **kwargs)

    def get_parameter_names(self) -> List[str]:
        return [name for name, param in self._parameters]

    def make_parameter_value_mapping(self, *args, **kwargs) -> Dict[str, Any]:
        mapping = {}
        args = deque(args)
        for name, param in self._parameters:
            annotation = param.annotation
            default = param.default
            kind = param.kind

            if len(args) > 0:
                if kind == Parameter.KEYWORD_ONLY:
                    raise TypeError(f"Usecase's parameter {name} is keyword-only parameter")
                value = args.popleft()
            elif name in kwargs:
                value = kwargs.pop(name)
            elif default is not Signature.empty:
                value = default
            else:
                raise TypeError(f"Usecase's parameter {name} is missing.")

            if not isinstance(value, annotation):
                raise TypeError(f"Usecase's parameter {name} should be {annotation.__name__}")
            mapping[name] = value

        return mapping
