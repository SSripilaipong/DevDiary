from typing import Dict

from lambler.base.response import LamblerResponse


class DynamodbEventResponse(LamblerResponse):
    def to_dict(self) -> Dict:
        return {}


class DynamodbEventBatchResponse(LamblerResponse):
    def to_dict(self) -> Dict:
        return {
            "batchItemFailures": [],
        }
