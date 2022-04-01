from typing import TypeVar, Callable, Any, Type, Optional

from chamber.usecase.parameter import ParameterValidator

T = TypeVar("T", bound=Callable)


class Usecase:
    def __init__(self, func: Callable):
        self._return_type = self._extract_return_type(func)
        self._parameter_validator = ParameterValidator.from_function(func)
        self._default_func = func

        self._func = self.__default_func_call

    def __call__(self, *args, **kwargs) -> Any:
        return self._func(*args, **kwargs)

    def __default_func_call(self, *args, **kwargs) -> Any:
        self._parameter_validator.validate_parameter(*args, **kwargs)
        return self._default_func(*args, **kwargs)

    def override_function(self, func: Callable):
        self._func = func

    def get_function(self) -> Callable:
        return self._func

    def _extract_return_type(self, func: Callable) -> Optional[Type]:
        annotations = getattr(func, "__annotations__", {})
        if "return" not in annotations:
            raise TypeError("Usecase should have a return type.")
        return_type = annotations["return"]
        assert isinstance(return_type, type) or return_type is None  # TODO: properly raise error
        return return_type

    @property
    def return_type(self) -> Type:
        return self._return_type

    def get_parameter_validator(self) -> ParameterValidator:
        return self._parameter_validator
