from pytest import raises
from domain.identity.value_object.password import Password
from domain.identity.value_object.password.exception import PasswordMustContainRequiredCharactersException, \
    PasswordTooShortException, PasswordTooLongException


def test_should_create_password():
    Password("Aa12345678")


def test_should_raise_PasswordMustContainRequiredCharactersException_when_no_digits():
    with raises(PasswordMustContainRequiredCharactersException):
        Password("Aaaaaaaaaaaaaa")


def test_should_raise_PasswordMustContainRequiredCharactersException_when_no_uppercase():
    with raises(PasswordMustContainRequiredCharactersException):
        Password("aaaaaaaaaaaaaa")


def test_should_raise_PasswordMustContainRequiredCharactersException_when_no_lowercase():
    with raises(PasswordMustContainRequiredCharactersException):
        Password("AAAAAAAAAAAAAA")


def test_should_raise_PasswordTooShortException_for_password_7_characters_long():
    with raises(PasswordTooShortException):
        Password("Aa12345")


def test_should_raise_PasswordTooLongException_for_password_65_characters_long():
    with raises(PasswordTooLongException):
        Password("1A"+"a"*63)
