from typing import Dict, Any

from pydantic import BaseModel

from lambler.api_gateway.method import RequestMethodEnum
from lambler.base.event import LamblerEvent


class APIGatewayEvent(BaseModel, LamblerEvent):
    path: str
    method: RequestMethodEnum
    query_string_parameters: Dict[str, Any]
    headers: Dict[str, str]
    body: str
