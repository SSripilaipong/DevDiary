from typing import List, Dict, Any

from lambler.base.handler import PatternMatcher
from lambler.base.response import LamblerResponse


class Lambler:
    def __init__(self):
        self.__patterns: List[PatternMatcher] = []

    def __call__(self, event: Dict, context: Any) -> Any:
        response = self.call_raw_response(event, context)

        if isinstance(response, LamblerResponse):
            return response.to_dict()
        return response

    def call_raw_response(self, event: Dict, context: Any) -> LamblerResponse:
        handler = self.__get_matched_handler(event, context)
        return handler.handle()

    def include_pattern(self, pattern: PatternMatcher):
        self.__patterns.append(pattern)

    def __get_matched_handler(self, event: Dict, context: Any):
        for pattern in self.__patterns:
            matched = pattern.match(event, context)
            if matched is not None:
                return matched
        raise NotImplementedError()
