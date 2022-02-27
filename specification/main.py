from devdiary.specification.registration import RegistrationSpecification
from devdiary.specification.registration.dsl import RegistrationDsl
from devdiary.specification.registration.driver import RegistrationDriver


class MyDriver(RegistrationDriver):
    def submit_registration(self, username: str, password: str, display_name: str, email: str):
        pass

    def confirm_registration_by_email(self, email: str):
        pass

    def login_with_username_and_password(self, username: str, password: str):
        pass

    def get_current_username(self) -> str:
        return "MyUsername"


def main():
    RegistrationSpecification(RegistrationDsl(MyDriver())).run_test()
    print('end')


if __name__ == '__main__':
    main()
