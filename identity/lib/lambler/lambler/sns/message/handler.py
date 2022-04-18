from typing import Callable

from lambler.base.handler import Handler
from lambler.sns.message.response import SNSMessageResponse


class SNSMessageHandler(Handler):
    def __init__(self, handle: Callable):
        self._handle = handle

    def handle(self) -> SNSMessageResponse:
        self._handle()
        return SNSMessageResponse()
