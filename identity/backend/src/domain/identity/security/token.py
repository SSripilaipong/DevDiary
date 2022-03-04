from typing import Dict

import jwt

from domain.identity.security.exception import UserTokenValidationFailedException, UserTokenExpiredException
from domain.identity.user.user import User
from domain.registry import Registry


_EXPIRE_SECONDS = 20*60


def _issuer() -> str:
    return f"http://{Registry().APP_NAME}.devdiary.link"


def _audience() -> str:
    return f"devdiary-{Registry().APP_NAME}"


def generate_user_token(user: User) -> str:
    registry = Registry()
    payload = {
        "iss": _issuer(),
        "aud": _audience(),
        "exp": registry.clock.get_current_timestamp() + _EXPIRE_SECONDS,
        "sub": user.username.str(),
        "display_name": user.display_name,
    }

    return jwt.encode(payload, registry.secret_manager.get_private_key(), algorithm="RS512")


def get_username_from_user_token(token: str) -> str:
    """
    :raises:
        UserTokenValidationFailedException
        UserTokenExpiredException
    """
    payload = validate_user_token(token)
    return payload['sub']


def validate_user_token(token: str) -> Dict:
    """
    :raises:
        UserTokenValidationFailedException
        UserTokenExpiredException
    """
    registry = Registry()
    try:
        payload = jwt.decode(token, registry.secret_manager.get_public_key(), algorithms=["RS512"],
                             options={"verify_exp": False}, issuer=_issuer(), audience=_audience())
    except jwt.PyJWTError as e:
        raise UserTokenValidationFailedException(e)
    if payload['exp'] <= registry.clock.get_current_timestamp():
        raise UserTokenExpiredException()
    return payload
