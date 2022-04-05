from pydantic import BaseModel
from typing import Dict, Type

from chamber.data.model import DataModel
from lambler.api_gateway.exception import InvalidParameterError
from lambler.api_gateway.marker.json_body.parser.dict import DictParser
from lambler.api_gateway.marker.json_body.parser.chamber import ChamberParser
from lambler.api_gateway.marker.json_body.parser.parser import Parser
from lambler.api_gateway.marker.json_body.parser.pydantic import PydanticParser


class ParserFactory:
    def __init__(self):
        self._parsers: Dict[Type, Type[Parser]] = {}

    def add_parser(self, type_: Type, parser: Type[Parser]):
        if type_ not in self._parsers:
            self._parsers[type_] = parser
        else:
            raise NotImplementedError()

    def for_type(self, type_: Type) -> Parser:
        for parent, parser in self._parsers.items():
            if type_ is parent or (isinstance(type_, type) and issubclass(type_, parent)):
                return parser.from_type(type_)
        raise InvalidParameterError()


parser_factory = ParserFactory()
parser_factory.add_parser(dict, DictParser)
parser_factory.add_parser(Dict, DictParser)
parser_factory.add_parser(BaseModel, PydanticParser)
parser_factory.add_parser(DataModel, ChamberParser)
