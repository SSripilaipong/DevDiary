from typing import Union, Any, Optional


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


class UsecaseCallResultMocker:
    def __init__(self, call: UsecaseCallMocker):
        self._call = call

    def then_return(self, value: Any):
        self._call.result = value


class UsecaseMocker:
    def __init__(self):
        self._call: Optional[UsecaseCallMocker] = None

    def __call__(self) -> Union[Any, UsecaseCallMocker]:
        if self._call is None:
            self._call = UsecaseCallMocker(self)
            return self._call
        return self._call.result


def when(call: UsecaseCallMocker) -> UsecaseCallResultMocker:
    return UsecaseCallResultMocker(call)
