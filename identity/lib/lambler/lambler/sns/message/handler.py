from typing import Callable

from lambler.base.handler import Handler
from lambler.base.response import LamblerResponse
from lambler.sns.message.response import SNSMessageResponse


class SNSMessageHandler(Handler):
    def __init__(self, handle: Callable):
        self._handle = handle

    def handle(self) -> SNSMessageResponse:
        self._handle()
        return SNSMessageResponse()


class SNSMessageIgnorer(Handler):
    def handle(self) -> LamblerResponse:
        return SNSMessageResponse()
