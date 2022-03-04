from respec import Dsl

from devdiary.specification.registration.driver import RegistrationDriver


class RegistrationDsl(Dsl):
    driver: RegistrationDriver

    def register(self, username: str, password: str, display_name: str, email: str):
        self.driver.submit_registration(username, password, display_name, email)

    def confirm_registration(self, email: str):
        confirmation_code = self.driver.get_confirmation_code_from_email(email)
        self.driver.confirm_registration_by_email(email, confirmation_code)

    def login(self, username: str, password: str):
        self.driver.login_with_username_and_password(username, password)

    def verify_current_user(self, username: str):
        assert username == self.driver.get_current_username()
