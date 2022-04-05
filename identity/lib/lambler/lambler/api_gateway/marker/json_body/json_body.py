from typing import Type, Any, Optional

from lambler.api_gateway.endpoint.input import HTTPInputCollection
from lambler.api_gateway.exception import InvalidParameterError
from lambler.api_gateway.marker.json_body.parser import parser_factory, Parser
from lambler.base.function.marker import Marker


class JSONBody(Marker):
    def __init__(self):
        self._parser: Optional[Parser] = None

    def register_type(self, type_: Type):
        self._parser = parser_factory.for_type(type_)

    def extract_param(self, sources: HTTPInputCollection) -> Any:
        assert isinstance(sources, HTTPInputCollection)
        headers = sources.headers
        if headers.get('content-type') != 'application/json':
            raise InvalidParameterError()

        if self._parser is not None:
            return self._parser.parse(sources.body.to_dict())

        raise NotImplementedError()
