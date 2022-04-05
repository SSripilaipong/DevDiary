from typing import Type, Dict, Any, Optional

from lambler.api_gateway.marker.json_body.parser import parser_factory, Parser
from lambler.base.marker import Marker


class JSONBody(Marker):
    def __init__(self):
        self._parser: Optional[Parser] = None

    def register_type(self, type_: Type):
        self._parser = parser_factory.for_type(type_)

    def extract_param(self, data: Dict) -> Any:
        if self._parser is not None:
            return self._parser.parse(data)
        raise NotImplementedError()
