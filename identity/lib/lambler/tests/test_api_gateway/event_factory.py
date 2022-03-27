import json

from typing import Dict
from lambler.api_gateway.method import RequestMethodEnum


def simple_post_event(path: str, body_dict: Dict = None) -> Dict:
    body = "" if body_dict is None else json.dumps(body_dict)
    return {
        "path": path,
        "method": RequestMethodEnum.POST,
        "query_string_parameters": {},
        "headers": {},
        "body": body,
    }


def simple_get_event(path: str) -> Dict:
    return {
        "path": path,
        "method": RequestMethodEnum.GET,
        "query_string_parameters": {},
        "headers": {},
        "body": "",
    }
