import json

from typing import Dict

from abc import ABC, abstractmethod

from lambler.api_gateway.status import HTTPStatus
from lambler.base.response import LamblerResponse


class APIGatewayResponse(LamblerResponse, ABC):
    def __init__(self, status_code=None):
        self._status_code = status_code or HTTPStatus.OK

    @property
    def status_code(self) -> HTTPStatus:
        return self._status_code

    @property
    @abstractmethod
    def body(self) -> str:
        pass

    @property
    @abstractmethod
    def body_dict(self) -> Dict:
        pass

    def to_dict(self) -> Dict:
        return {
            "body": self.body,
        }


class HTTPResponse(APIGatewayResponse):
    def __init__(self, body="", status_code=None):
        super().__init__(status_code=status_code)
        self._body = body or ""

    @property
    def body(self) -> str:
        return self._body

    @property
    def body_dict(self) -> Dict:
        return json.loads(self._body)


class JSONResponse(APIGatewayResponse):
    def __init__(self, body=None, status_code=None):
        super().__init__(status_code=status_code)
        self._body = body or {}

    @property
    def body(self) -> str:
        return json.dumps(self._body)

    @property
    def body_dict(self) -> Dict:
        return self._body