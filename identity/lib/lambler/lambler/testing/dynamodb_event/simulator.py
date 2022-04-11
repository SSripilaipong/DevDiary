from boto3.dynamodb.types import TypeSerializer
from typing import Dict, Any

from lambler import Lambler
from lambler.dynamodb_event.data.view import DynamodbStreamView


class DynamodbEventSimulator:
    def __init__(self, lambler: Lambler, stream_view_type: DynamodbStreamView):
        self._lambler = lambler
        self._serializer = TypeSerializer()

    def insert(self, data: Dict[str, Any], partition_key: str, sort_key: str = None):
        keys = {}

        if partition_key not in data:
            raise NotImplementedError()
        keys[partition_key] = self._serializer.serialize(data[partition_key])

        if sort_key is not None:
            if sort_key not in data:
                raise NotImplementedError()
            keys[sort_key] = self._serializer.serialize(data[sort_key])

        serialized_data = {key: self._serializer.serialize(value) for key, value in data.items()}
        event = _simple_event("INSERT", keys, new_image=serialized_data)
        self._lambler(event, ...)


def _simple_event(event_name, keys, new_image):
    return {
        "Records": [
            {
                "eventID": "ABC123",
                "eventName": event_name,
                "eventVersion": "1.1",
                "eventSource": "aws:dynamodb",
                "awsRegion": "ap-southeast-1",
                "dynamodb": {
                    "ApproximateCreationDateTime": 1648808551.0,
                    "Keys": keys,
                    "NewImage": new_image,
                    "SequenceNumber": "28232500000000016381400609",
                    "SizeBytes": 123,
                    "StreamViewType": "NEW_IMAGE"
                },
                "eventSourceARN": "arn:aws:dynamodb:ap-southeast-1:123456789012:table/tableName/stream/2022-03-26T16:21:38.846"
            },
        ],
    }
