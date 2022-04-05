from http import HTTPStatus

from domain.identity.registration.exception import EmailAlreadyRegisteredException
from domain.identity.user.exception import UsernameAlreadyRegisteredException
from lambler.api_gateway.aws.event.version import AWSEventVersion
from lambler.api_gateway.marker import JSONBody
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
        return JSONResponse({"message": "Email already used"}, status_code=HTTPStatus.CONFLICT)
    except UsernameAlreadyRegisteredException:
        return JSONResponse({"message": "Username already used"}, status_code=HTTPStatus.CONFLICT)
    return JSONResponse({"message": "ok"}, status_code=HTTPStatus.CREATED)
