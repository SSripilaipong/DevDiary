from typing import Dict, Any, Optional

from pydantic import BaseModel, Field


class HttpContext(BaseModel):
    path: str
    method: str


class RequestContext(BaseModel):
    request_id: str = Field(..., alias="requestId")
    http: HttpContext
    stage: str


class ApiGatewayServiceEvent(BaseModel):
    raw_path: str = Field(..., alias="rawPath")
    raw_query_string: str = Field(..., alias="rawQueryString")
    request_context: RequestContext = Field(..., alias="requestContext")
    headers: Dict[str, str]

    query_string_parameters: Optional[Dict[str, Any]] = Field(default_factory=dict, alias="queryStringParameters")
    body: Optional[str] = ''
