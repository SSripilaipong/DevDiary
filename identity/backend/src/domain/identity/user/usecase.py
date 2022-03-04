from domain.identity.user.user import User
from domain.identity.authentication.token import get_username_from_user_token as _get_username_from_user_token
from domain.identity.value_object.username import Username
from domain.registry import Registry


def create_new_user_from_registered_email(email: str):
    """
    :raises:
        RegistrationNotFoundException: The registration is not found
    """
    registry = Registry()
    registration = registry.all_registrations.from_email(email)
    user = User.create(registration.username, registration.password_hashed, registration.display_name,
                       registration.email)
    registry.all_users.create(user)


def get_username_from_user_token(user_token: str) -> Username:
    return Username.create(_get_username_from_user_token(user_token))
