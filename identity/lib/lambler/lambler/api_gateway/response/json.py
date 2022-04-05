from typing import Dict

import json

from lambler.api_gateway.response.api_gateway import APIGatewayResponse


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