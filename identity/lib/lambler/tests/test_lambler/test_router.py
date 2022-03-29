from pytest import raises
from typing import Dict, Any

from lambler import Lambler
from lambler.base.handler import PatternMatcher, Handler


def test_should_raise_NotImplementedError_when_no_matchers():
    lambler = Lambler()
    with raises(NotImplementedError):
        lambler({}, ...)


def test_should_return_from_matched_handler():
    class MyHandler(Handler):
        def handle(self) -> Any:
            return "OK!"

    class MyPattern(PatternMatcher):
        def match(self, event: Dict, context: Any) -> MyHandler:
            return MyHandler()

    lambler = Lambler()
    lambler.include_pattern(MyPattern())

    assert lambler({}, ...) == "OK!"

