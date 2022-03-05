from pytest import raises
from domain.identity.value_object.email import Email
from domain.identity.value_object.email.exception import EmailPatternNotMatchedException


def test_should_create_email():
    Email('myname@devdiary.link')


def test_should_raise_error_when_email_has_no_at_sign():
    with raises(EmailPatternNotMatchedException):
        Email('myname.devdiary.link')


def test_should_raise_error_when_email_has_no_extension():
    with raises(EmailPatternNotMatchedException):
        Email('myname@devdiary')


def test_should_raise_error_when_email_has_no_username():
    with raises(EmailPatternNotMatchedException):
        Email('@devdiary.link')
