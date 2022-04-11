from typing import Dict, List

from lambler.base.response import LamblerResponse


class DynamodbEventResponse(LamblerResponse):
    def to_dict(self) -> Dict:
        return {}


class DynamodbEventBatchResponse(LamblerResponse):
    def __init__(self, failed_item_ids: List[str]):
        self._failed_item_ids = [{"itemIdentifier": item_id} for item_id in failed_item_ids]

    def to_dict(self) -> Dict:
        return {
            "batchItemFailures": self._failed_item_ids,
        }
