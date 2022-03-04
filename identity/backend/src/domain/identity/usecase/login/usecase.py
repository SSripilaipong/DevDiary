from domain.identity.security.password import check_password
from domain.identity.security.token import generate_user_token
from domain.identity.usecase.login.exception import LoginFailedException
from domain.identity.value_object.username import Username, InvalidUsernameException
from domain.registry import Registry


def login_with_username_and_password(username: str, password: str) -> str:
    """
    :raises:
        LoginFailedException
    """
    try:
        user = Registry().all_users.from_username(Username.create(username))
    except InvalidUsernameException:
        raise LoginFailedException()
    if check_password(password, user.password_hashed):
        return generate_user_token(user)
    raise LoginFailedException()
