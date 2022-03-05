from domain.identity.security.password import check_password
from domain.identity.security.token import generate_user_token
from domain.identity.usecase.login.exception import LoginFailedException
from domain.identity.value_object.password import Password
from domain.identity.value_object.username import Username
from domain.identity.value_object.username.exception import InvalidUsernameException
from domain.registry import Registry


def login_with_username_and_password(username: str, password: str) -> str:
    """
    :raises:
        LoginFailedException
    """
    try:
        user = Registry().all_users.from_username(Username(username))
    except InvalidUsernameException:
        raise LoginFailedException()
    if check_password(Password.as_is(password), user.password_hashed):
        return generate_user_token(user)
    raise LoginFailedException()
