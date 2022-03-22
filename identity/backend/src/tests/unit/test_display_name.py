from pytest import raises
from domain.identity.value_object.display_name import DisplayName
from domain.identity.value_object.display_name.exception import (
    DisplayNameTooLongException, DisplayNameTooShortException,
)


def test_should_create_display_name():
    DisplayName('aaaa#bbbb')


def test_should_raise_DisplayNameTooShortException_for_display_name_3_characters_long():
    with raises(DisplayNameTooShortException):
        DisplayName('a'*3)


def test_should_raise_DisplayNameTooLongException_for_display_name_17_characters_long():
    with raises(DisplayNameTooLongException):
        DisplayName('a'*17)
