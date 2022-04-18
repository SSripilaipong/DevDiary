from typing import Optional, Type, Any

from lambler.base.data.parser import Parser, parser_factory
from lambler.base.data.parser.exception import DataParsingError
from lambler.base.function.marker import Marker
from lambler.sns.message.input.collection import SNSMessageInputCollection


class MessageBody(Marker):
    def __init__(self):
        self._parser: Optional[Parser] = None

    def register_type(self, type_: Type):
        try:
            self._parser = parser_factory.for_type(type_)
        except TypeError:
            raise NotImplementedError()

    def extract_param(self, data: SNSMessageInputCollection) -> Any:
        data = data.body.to_str()
        if self._parser is None:
            raise NotImplementedError()
        try:
            return self._parser.parse(data)
        except DataParsingError as e:
            raise e
