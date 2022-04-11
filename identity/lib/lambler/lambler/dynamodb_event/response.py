from typing import Dict, List

from lambler.base.response import LamblerResponse


class DynamodbEventResponse(LamblerResponse):
    def to_dict(self) -> Dict:
        return {}


class DynamodbEventBatchResponse(LamblerResponse):
    def __init__(self, failed_item_ids: List[str]):
        self._failed_item_ids = failed_item_ids

    def to_dict(self) -> Dict:
        return {
            "batchItemFailures": [{"itemIdentifier": item_id} for item_id in self._failed_item_ids],
        }

    @property
    def failed_item_ids(self) -> List[str]:
        return self._failed_item_ids.copy()

    @classmethod
    def from_dict(cls, response: Dict) -> 'DynamodbEventBatchResponse':
        failures = response.get("batchItemFailures", [])

        ids = []
        for item in failures:
            id_ = item.get("itemIdentifier", None)
            if id_ is None:
                raise NotImplementedError()
            ids.append(id_)
        return cls(ids)
