from typing import Dict

from lambler.api_gateway.status import HTTPStatus


class HTTPResponse:
    def __init__(self):
        self._status_code = None

    @property
    def status_code(self) -> HTTPStatus:
        return self._status_code

    def json(self) -> Dict:
        pass
