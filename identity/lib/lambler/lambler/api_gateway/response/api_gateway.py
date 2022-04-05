from http import HTTPStatus

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