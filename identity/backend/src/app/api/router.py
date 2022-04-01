import json

from typing import Dict

from domain.identity.registration.exception import EmailAlreadyRegisteredException
from lambler.api_gateway.aws.version import AWSEventVersion
from lambler.api_gateway.endpoint.marker import JSONBody
from lambler.api_gateway.response import JSONResponse
from lambler.api_gateway.router import APIGatewayRouter

from domain.identity.usecase.registration import register_user

from app.api.request import RegistrationRequest


router = APIGatewayRouter(event_version=AWSEventVersion.V2)


@router.post("/users/register")
def register(request: RegistrationRequest = JSONBody()):
    try:
        _ = register_user(request.username, request.password, request.display_name, request.email)
    except EmailAlreadyRegisteredException:
        return JSONResponse({"message": "Email already used"}, status_code=409)
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
