from typing import Any, Type, Optional

from lambler.base.data.parser import parser_factory, Parser
from lambler.base.data.parser.exception import DataParsingError
from lambler.base.function.input import FunctionInputSourceCollection
from lambler.base.function.marker import Marker
from lambler.dynamodb_event.input.new_image import DynamodbEventNewImageInputSource


class EventBody(Marker):
    def __init__(self):
        self._parser: Optional[Parser] = None

    def register_type(self, type_: Type):
        try:
            self._parser = parser_factory.for_type(type_)
        except TypeError:
            raise NotImplementedError()

    def extract_param(self, data: FunctionInputSourceCollection) -> Any:
        new_image = data.of(DynamodbEventNewImageInputSource)
        data = new_image.to_dict()
        if self._parser is None:
            raise NotImplementedError()
        try:
            return self._parser.parse(data)
        except DataParsingError:
            raise NotImplementedError()
