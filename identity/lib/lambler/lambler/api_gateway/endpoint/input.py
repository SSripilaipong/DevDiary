from json import JSONDecodeError

import json

from typing import Dict, Optional

from lambler.api_gateway.event import APIGatewayEvent
from lambler.api_gateway.exception import InvalidParameterError
from lambler.base.source import FunctionInputSourceCollection, FunctionInputSource


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


class HeaderInputSource(FunctionInputSource):
    def __init__(self, headers: Dict[str, str]):
        self._headers = headers

    @classmethod
    def from_event(cls, event: APIGatewayEvent) -> 'HeaderInputSource':
        return cls(event.headers)

    def get(self, key: str) -> Optional[str]:
        return self._headers.get(key, None)


class HTTPInputCollection(FunctionInputSourceCollection):
    @classmethod
    def from_event(cls, event: APIGatewayEvent) -> 'HTTPInputCollection':
        return cls({
            BodyInputSource: BodyInputSource.from_event(event),
            HeaderInputSource: HeaderInputSource.from_event(event),
        })

    @property
    def headers(self) -> HeaderInputSource:
        return self.of(HeaderInputSource)

    @property
    def body(self) -> BodyInputSource:
        return self.of(BodyInputSource)
