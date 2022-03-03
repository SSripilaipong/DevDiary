import sys

from respec import Verification
from devdiary.specification.registration import RegistrationSpecification

from tests.domain.registration.driver import DomainRegistrationDriver


def main():
    return not Verification().include(
        RegistrationSpecification.using(DomainRegistrationDriver()),
    ).verify().wasSuccessful()


if __name__ == "__main__":
    sys.exit(main())
