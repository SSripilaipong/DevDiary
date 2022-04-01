from app.main import handler
from chamber.testing import mock_usecase, when
from domain.identity.registration.registration import Registration
from domain.identity.usecase.registration import register_user
from domain.identity.value_object.display_name import DisplayName
from domain.identity.value_object.email import Email
from domain.identity.value_object.password import Password
from domain.identity.value_object.username import Username
from lambler.api_gateway.aws.version import AWSEventVersion
from lambler.testing.api_gateway.requester import HTTPRequester


@mock_usecase(register_user)
def test_should_call_register_user_usecase():
    when(register_user(Username.as_is("cpeng"), Password.as_is("CPEng12345678"),
                       DisplayName.as_is("cpeng"), Email.as_is("cpeng@devdiary.link"))) \
        .then_return(Registration.create(Username.as_is(""), b"", DisplayName.as_is(""), Email.as_is(""),
                                         confirmation_code=""))

    requester = HTTPRequester(handler, event_version=AWSEventVersion.V2)
    requester.post("/users/register", {"username": "cpeng", "password": "CPEng12345678", "displayName": "cpeng",
                                       "email": "cpeng@devdiary.link"})
