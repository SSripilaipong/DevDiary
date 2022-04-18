from lambler.base.data.parser.exception import DataParsingError
from lambler.base.function import MarkedFunction
from lambler.base.function.input import FunctionInputSourceCollection
from lambler.base.handler import Handler
from lambler.base.response import LamblerResponse
from lambler.sns.message.response import SNSMessageResponse


class SNSMessageHandler(Handler):
    def __init__(self, handle: MarkedFunction, sources: FunctionInputSourceCollection):
        self._handle = handle
        self._sources = sources

    def handle(self) -> SNSMessageResponse:
        try:
            self._handle.execute(self._sources)
        except DataParsingError as e:
            raise e
        except Exception:
            raise NotImplementedError()
        return SNSMessageResponse()


class SNSMessageIgnorer(Handler):
    def handle(self) -> LamblerResponse:
        return SNSMessageResponse()
