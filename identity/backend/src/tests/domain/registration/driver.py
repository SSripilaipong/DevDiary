from devdiary.specification.registration import RegistrationDriver

from domain.identity.registration.usecase import register_user, confirm_registration
from domain.identity.login.usecase import login_with_username_and_password
from domain.identity.user.usecase import get_username_from_user_token


class DomainRegistrationDriver(RegistrationDriver):
    def __init__(self, user_token: str = None):
        self._user_token = user_token

    def submit_registration(self, username: str, password: str, display_name: str, email: str):
        register_user(username, password, display_name, email)

    def confirm_registration_by_email(self, email: str):
        confirm_registration(email)

    def login_with_username_and_password(self, username: str, password: str):
        self._user_token = login_with_username_and_password(username, password)

    def get_current_username(self) -> str:
        return get_username_from_user_token(self._user_token)
