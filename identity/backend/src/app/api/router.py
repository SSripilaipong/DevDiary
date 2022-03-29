import json

from typing import Dict

from lambler.api_gateway.aws.version import AWSEventVersion
from lambler.api_gateway.endpoint.marker import JSONBody
from lambler.api_gateway.router import APIGatewayRouter

from domain.identity.usecase.registration import register_user
from domain.identity.value_object.display_name import DisplayName
from domain.identity.value_object.email import Email
from domain.identity.value_object.password import Password
from domain.identity.value_object.username import Username

from app.api.request import RegistrationRequest


router = APIGatewayRouter(event_version=AWSEventVersion.V2)


@router.post("/users/register")
def register(request: RegistrationRequest = JSONBody()):
    _ = register_user(request.username, request.password, request.display_name, request.email)
    return created_response("ok")


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
