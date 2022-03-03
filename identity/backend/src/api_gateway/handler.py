from typing import Dict, Any
import json


def handle_event(method: str, operation: str, headers: Dict[str, str],
                 query_string_parameters: Dict[str, Any], body: str) -> Dict:
    print(repr(method), repr(operation), repr(headers), repr(query_string_parameters), repr(body))
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps({
            "message": "OK!",
        }),
    }
