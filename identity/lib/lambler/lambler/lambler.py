from typing import List, Dict, Any

from lambler.base.handler import PatternMatcher


class Lambler:
    def __init__(self):
        self.__patterns: List[PatternMatcher] = []

    def __call__(self, event: Dict, context: Any) -> Any:
        for pattern in self.__patterns:
            matched = pattern.match(event, context)
            if matched is not None:
                break
        else:
            return None  # TODO: must change

        return matched.handle()

    def include_pattern(self, pattern: PatternMatcher):
        self.__patterns.append(pattern)
