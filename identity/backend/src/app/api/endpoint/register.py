import json
from typing import Dict, Any

from pydantic import BaseModel

from domain.identity.value_object.display_name import DisplayName
from lambler.api_gateway.endpoint import Endpoint
from domain.identity.usecase.registration import register_user
from domain.identity.value_object.email import Email
from domain.identity.value_object.password import Password
from domain.identity.value_object.username import Username


class RegisterEndpoint(Endpoint):

    def process(self, headers: Dict[str, str], query: Dict[str, Any], body: str):
        if headers.get('content-type', None) != 'application/json':
            return unprocessable_entity_response("json content required")

        request = RegistrationRequest(**json_body(body))
        if body is None:
            return unprocessable_entity_response("cannot process body")

        _ = register_user(
            Username(request.username), Password(request.password), DisplayName(request.display_name),
            Email(request.email),
        )
        return created_response("ok")


class RegistrationRequest(BaseModel):
    username: str
    password: str
    display_name: str
    email: str


def unprocessable_entity_response(message: str) -> Dict:
    return {
        "statusCode": 422,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps({
            "message": message,
        }),
    }


def created_response(message: str) -> Dict:
    return {
        "statusCode": 201,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps({
            "message": message,
        }),
    }


def json_body(body: str) -> Dict[str, Any]:
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        pass
