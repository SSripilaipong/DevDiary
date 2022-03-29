from typing import Dict, Any

from lambler import Lambler
from lambler.base.handler import PatternMatcher, Handler


def test_should_return_None_when_no_matchers():
    assert Lambler()() is None


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

