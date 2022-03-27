from typing import Dict, Any

from pydantic import BaseModel

from lambler.api_gateway.method import RequestMethodEnum


class APIGatewayEvent(BaseModel):
    path: str
    method: RequestMethodEnum
    query_string_parameters: Dict[str, Any]
    headers: Dict[str, str]
    body: str
