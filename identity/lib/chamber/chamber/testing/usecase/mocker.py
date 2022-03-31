from typing import Union, Any, Optional, Type

from chamber.usecase import Usecase


class UsecaseCallMocker:
    def __init__(self, mocker: 'UsecaseMocker'):
        self._mocker = mocker
        self._result = None

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        self._result = value

    @property
    def expected_return_type(self) -> Type:
        return self._mocker.return_type


class UsecaseCallResultMocker:
    def __init__(self, call: UsecaseCallMocker):
        self._call = call

    def then_return(self, value: Any):
        expected_type = self._call.expected_return_type
        if not isinstance(value, expected_type):
            raise TypeError(f"then_return() should be called with value of type {expected_type.__name__}.")
        self._call.result = value


class UsecaseMocker:
    def __init__(self, usecase: Usecase):
        self._usecase = usecase
        self._call: Optional[UsecaseCallMocker] = None

    def __call__(self) -> Union[Any, UsecaseCallMocker]:
        if self._call is None:
            self._call = UsecaseCallMocker(self)
            return self._call
        return self._call.result

    @property
    def return_type(self) -> Type:
        return self._usecase.return_type


def when(call: Any) -> UsecaseCallResultMocker:
    if not isinstance(call, UsecaseCallMocker):
        raise TypeError("when() should be used with mocked usecase.")
    return UsecaseCallResultMocker(call)
