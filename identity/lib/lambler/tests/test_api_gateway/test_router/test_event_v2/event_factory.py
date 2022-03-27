import os
from typing import Dict
import json


def simple_post_event(path: str) -> Dict:
    with open(os.path.join(os.path.dirname(__file__), "event-v2.json")) as file:
        data = json.load(file)
    data["rawPath"] = path
    data["requestContext"]["http"]["method"] = "POST"
    data["requestContext"]["http"]["path"] = path
    return data
