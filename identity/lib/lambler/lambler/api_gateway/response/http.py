import json

from typing import Dict

from lambler.api_gateway.response.api_gateway import APIGatewayResponse


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