from http import HTTPStatus

import json

from typing import Dict

from abc import ABC, abstractmethod

from lambler.base.response import LamblerResponse


class APIGatewayResponse(LamblerResponse, ABC):
    def __init__(self, status_code: int = None, headers: Dict = None, is_base64_encoded: bool = False):
        self._status_code = status_code or HTTPStatus.OK
        self._headers = headers or {}
        self._is_base64_encoded = is_base64_encoded

    @property
    def status_code(self) -> int:
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
            "isBase64Encoded": self._is_base64_encoded,
            "body": self.body,
            "statusCode": self.status_code,
            "headers": self._headers,
        }


class HTTPResponse(APIGatewayResponse):
    def __init__(self, body="", status_code: int = None):
        super().__init__(status_code=status_code)
        self._body = body or ""

    @property
    def body(self) -> str:
        return self._body

    @property
    def body_dict(self) -> Dict:
        return json.loads(self._body)


class JSONResponse(APIGatewayResponse):
    def __init__(self, body=None, status_code=None, headers=None):
        headers = headers or {}
        headers.update({"content-type": "application/json"})

        super().__init__(status_code=status_code, headers=headers)
        self._body = body or {}

    @property
    def body(self) -> str:
        return json.dumps(self._body)

    @property
    def body_dict(self) -> Dict:
        return self._body
