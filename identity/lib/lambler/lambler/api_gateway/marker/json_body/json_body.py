import json
from json import JSONDecodeError

from typing import Type, Any, Optional, Dict

from lambler.api_gateway.exception import InvalidParameterError
from lambler.base.source import FunctionInputSource, FunctionInputSourceCollection
from lambler.api_gateway.event import APIGatewayEvent
from lambler.api_gateway.marker.json_body.parser import parser_factory, Parser
from lambler.base.marker import Marker


class HeaderInputSource(FunctionInputSource):
    def __init__(self, headers: Dict[str, str]):
        self._headers = headers

    @classmethod
    def from_event(cls, event: APIGatewayEvent) -> 'HeaderInputSource':
        return cls(event.headers)

    def get(self, key: str) -> Optional[str]:
        return self._headers.get(key, None)


class BodyInputSource(FunctionInputSource):
    def __init__(self, event: APIGatewayEvent):
        self._event = event

    @classmethod
    def from_event(cls, event: APIGatewayEvent) -> 'BodyInputSource':
        return cls(event)  # lazy casting

    def to_dict(self) -> Dict:
        try:
            body = json.loads(self._event.body)
        except JSONDecodeError:
            raise InvalidParameterError()

        if not isinstance(body, dict):
            raise InvalidParameterError()
        return body


class JSONBody(Marker):
    def __init__(self):
        self._parser: Optional[Parser] = None

    def register_type(self, type_: Type):
        self._parser = parser_factory.for_type(type_)

    def extract_param(self, sources: FunctionInputSourceCollection) -> Any:
        headers = sources.of(HeaderInputSource)
        if headers.get('content-type') != 'application/json':
            raise InvalidParameterError()

        if self._parser is not None:
            return self._parser.parse(sources.of(BodyInputSource).to_dict())

        raise NotImplementedError()
