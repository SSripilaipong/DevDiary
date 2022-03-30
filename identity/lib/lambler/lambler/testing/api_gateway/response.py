import json

from typing import Dict

from lambler.api_gateway.status import HTTPStatus


class HTTPResponse:
    def __init__(self, content=None, status_code=None):
        self._content = content
        self._status_code = status_code or HTTPStatus.OK

    @property
    def status_code(self) -> HTTPStatus:
        return self._status_code

    def json(self) -> Dict:
        return json.loads(self._content)
