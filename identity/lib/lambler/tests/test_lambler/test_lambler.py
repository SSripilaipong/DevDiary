from typing import Dict, Any

from lambler import Lambler
from lambler.base.handler import PatternMatcher, Handler
from lambler.base.response import LamblerResponse


def test_should_return_None_when_no_matchers():
    lambler = Lambler()
    return lambler({}, ...) is None


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


def test_should_return_from_matched_handler_among_many():
    class MyHandler1(Handler):
        def handle(self) -> Any:
            return "OK!"

    class MyPattern1(PatternMatcher):
        def match(self, event: Dict, context: Any) -> MyHandler1:
            if event["type"] == 1:
                return MyHandler1()

    class MyHandler2(Handler):
        def handle(self) -> Any:
            return "GREAT!"

    class MyPattern2(PatternMatcher):
        def match(self, event: Dict, context: Any) -> MyHandler2:
            if event["type"] == 2:
                return MyHandler2()

    lambler = Lambler()
    lambler.include_pattern(MyPattern1())
    lambler.include_pattern(MyPattern2())

    assert lambler({"type": 1}, ...) == "OK!"
    assert lambler({"type": 2}, ...) == "GREAT!"


def test_should_convert_LamblerResponse_to_dict():
    class MyResponse(LamblerResponse):
        def to_dict(self) -> Dict:
            return {"Hello": "World"}

    class MyHandler(Handler):
        def handle(self) -> Any:
            return MyResponse()

    class MyPattern(PatternMatcher):
        def match(self, event: Dict, context: Any) -> MyHandler:
            return MyHandler()

    lambler = Lambler()
    lambler.include_pattern(MyPattern())

    assert lambler({}, ...) == {"Hello": "World"}
