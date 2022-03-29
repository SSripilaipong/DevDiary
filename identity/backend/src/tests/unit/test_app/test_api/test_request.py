from app.api.request import RegistrationRequest


def test_should_accept_registration_request():
    data = {"username": "cpeng", "password": "CPEng12345678",
            "displayName": "CPEngineer", "email": "vappakarat@gmail.com"}
    request = RegistrationRequest.from_dict(data)
    assert request.username.str() == "cpeng"
    assert request.password.str() == "CPEng12345678"
    assert request.display_name.str() == "CPEngineer"
    assert request.email.str() == "vappakarat@gmail.com"
