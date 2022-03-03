from typing import Dict, Any, Optional

from pydantic import BaseModel, Field

from api_gateway.handler import handle_event
from lambda_handler.service_event.abstract import ServiceEvent


class HttpContext(BaseModel):
    path: str
    method: str


class RequestContext(BaseModel):
    request_id: str = Field(..., alias="requestId")
    http: HttpContext
    stage: str


class ApiGatewayServiceEvent(BaseModel, ServiceEvent):
    raw_path: str = Field(..., alias="rawPath")
    raw_query_string: str = Field(..., alias="rawQueryString")
    request_context: RequestContext = Field(..., alias="requestContext")
    headers: Dict[str, str]

    query_string_parameters: Optional[Dict[str, Any]] = Field(default_factory=dict, alias="queryStringParameters")
    body: Optional[str] = ''

    @classmethod
    def match(cls, raw_event: Dict) -> bool:
        return raw_event.get('headers', {}).get('x-service-operation', None) is not None

    @classmethod
    def from_raw_event(cls, raw_event: Dict) -> 'ServiceEvent':
        return cls(**raw_event)

    def handle(self) -> Any:
        operation = self.headers['x-service-operation']
        return handle_event(self.request_context.http.method, operation, self.headers,
                            self.query_string_parameters, self.body)
