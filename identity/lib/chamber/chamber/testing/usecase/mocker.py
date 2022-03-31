from typing import Union, Any, Optional, Type

from chamber.testing.exception import UnusedMockException
from chamber.usecase import Usecase


class UsecaseCallMocker:
    def __init__(self, mocker: 'UsecaseMocker'):
        self._mocker = mocker
        self._result = None
        self._is_called = False

    def get_result(self):
        self._is_called = True
        return self._result

    def set_result(self, value):
        self._result = value

    def is_called(self) -> bool:
        return self._is_called

    def add_to_mocker(self):
        self._mocker.add_mocked_call(self)

    @property
    def expected_return_type(self) -> Type:
        return self._mocker.return_type


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


class UsecaseMocker:
    def __init__(self, usecase: Usecase):
        self._usecase = usecase
        self._call: Optional[UsecaseCallMocker] = None

    def __call__(self, *args, **kwargs) -> Union[Any, UsecaseCallMocker]:
        if self._call is None:
            return UsecaseCallMocker(self)
        return self._call.get_result()

    def add_mocked_call(self, call: 'UsecaseCallMocker'):
        self._call = call  # TODO: make support for multiple calls

    @property
    def return_type(self) -> Type:
        return self._usecase.return_type

    def raise_unused_mock(self):
        if self._call is not None and not self._call.is_called():
            raise UnusedMockException("Mocked when() clause unused.")


def when(call: Any) -> UsecaseCallResultMocker:
    if not isinstance(call, UsecaseCallMocker):
        raise TypeError("when() should be used with mocked usecase.")
    call.add_to_mocker()
    return UsecaseCallResultMocker(call)
