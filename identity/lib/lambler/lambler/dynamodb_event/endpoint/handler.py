from typing import Callable

from lambler.base.handler import Handler
from lambler.dynamodb_event.endpoint.parameter import ParameterInjection
from lambler.dynamodb_event.data.event import DynamodbEvent
from lambler.dynamodb_event.response import DynamodbEventResponse
from lambler.dynamodb_event.data.type import DynamodbEventType


class DynamodbEventHandler(Handler):
    def __init__(self, handle: Callable, event: DynamodbEvent, param_injection: ParameterInjection):
        self._handle = handle
        self._event = event

        self._param_injection = param_injection

    @classmethod
    def create(cls, method: DynamodbEventType, handle: Callable, event: DynamodbEvent) -> 'DynamodbEventHandler':
        return cls(handle, event, ParameterInjection.from_handle_function(handle))

    def handle(self) -> DynamodbEventResponse:
        params = self._param_injection.extract_params(self._event)
        self._handle(**params)
        return DynamodbEventResponse()