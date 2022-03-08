import json
from typing import Dict, Any

from lambler.api_gateway.endpoint import Endpoint


class AlwaysOkEndpoint(Endpoint):
    def process(self, headers: Dict[str, str], query: Dict[str, Any], body: str):
        print(repr(headers), repr(query), repr(body))
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps({
                "message": "OK!",
            }),
        }
