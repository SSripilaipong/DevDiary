from typing import Union, Any, Optional, Type, List, Dict, Tuple

from chamber.testing.exception import UnusedMockException
from chamber.usecase import Usecase


class UsecaseCallMocker:
    def __init__(self, mocker: 'UsecaseMocker', param_tuple: Tuple):
        self._mocker = mocker
        self._param_tuple = param_tuple
        self._result = None
        self._exception = None
        self._is_called = False

    def get_result(self):
        self._is_called = True
        if self._exception is not None:
            raise self._exception
        return self._result

    def set_result(self, value):
        self._result = value

    def is_called(self) -> bool:
        return self._is_called

    def add_to_mocker(self):
        self._mocker.add_mocked_call(self)

    @property
    def param_tuple(self) -> Tuple:
        return self._param_tuple

    @property
    def expected_return_type(self) -> Type:
        return self._mocker.return_type

    def set_exception(self, exception: BaseException):
        self._exception = exception


class UsecaseCallResultMocker:
    def __init__(self, call: UsecaseCallMocker):
        self._call = call

    def then_return(self, value: Any):
        expected_type = self._call.expected_return_type
        if expected_type is None:
            if value is not None:
                raise TypeError("then_return() accepts only None, since the usecase function only return None.")
        elif not isinstance(value, expected_type):
            raise TypeError(f"then_return() should be called with value of type {expected_type.__name__}.")
        self._call.set_result(value)

    def then_raise(self, exception: BaseException):
        if not isinstance(exception, BaseException):
            raise NotImplementedError()
        self._call.set_exception(exception)


class UsecaseMocker:
    def __init__(self, usecase: Usecase, params: List[str]):
        self._usecase = usecase
        self._params = params
        self._calls: Dict[Tuple, UsecaseCallMocker] = {}

    def __call__(self, *args, **kwargs) -> Union[Any, UsecaseCallMocker]:
        param_tuple = self._get_param_tuple(args, kwargs)
        mocked_call = self._calls.get(param_tuple, None)
        if mocked_call is None:
            return UsecaseCallMocker(self, param_tuple)
        return mocked_call.get_result()

    def _get_param_tuple(self, args, kwargs) -> Tuple:
        validator = self._usecase.get_parameter_validator()
        mapping = validator.make_parameter_value_mapping(*args, **kwargs)
        param_tuple = tuple(mapping[name] for name in self._params)
        return param_tuple

    def add_mocked_call(self, call: 'UsecaseCallMocker'):
        self._calls[call.param_tuple] = call

    @property
    def return_type(self) -> Type:
        return self._usecase.return_type

    def raise_unused_mock(self):
        for call in self._calls.values():
            if not call.is_called():
                raise UnusedMockException("Mocked when() clause unused.")

    @classmethod
    def from_usecase(cls, usecase: Usecase):
        validator = usecase.get_parameter_validator()
        params = validator.get_parameter_names()
        return cls(usecase, params)


def when(call: Any) -> UsecaseCallResultMocker:
    if not isinstance(call, UsecaseCallMocker):
        raise TypeError("when() should be used with mocked usecase.")
    call.add_to_mocker()
    return UsecaseCallResultMocker(call)
