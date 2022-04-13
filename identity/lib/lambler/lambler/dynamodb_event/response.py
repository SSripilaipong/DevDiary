from typing import Dict, List

from lambler.base.response import LamblerResponse


class DynamodbEventResponse(LamblerResponse):
    def __init__(self, item_id: str, success: bool):
        self._item_id = item_id
        self._success = success

    def to_dict(self) -> Dict:
        return {
            "itemId": self._item_id,
            "success": self._success,
        }

    @property
    def item_id(self) -> str:
        return self._item_id

    @property
    def success(self) -> bool:
        return self._success


class DynamodbEventBatchResponse(LamblerResponse):
    def __init__(self, failed_item_ids: List[str]):
        self._failed_item_ids = failed_item_ids

    def to_dict(self) -> Dict:
        return {
            "batchItemFailures": [{"itemIdentifier": item_id} for item_id in self._failed_item_ids],
        }

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

    def all_success(self) -> bool:
        return self._failed_item_ids == []
