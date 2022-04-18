def simple_insert_event(body=None, event_id=None):
    return _simple_event("INSERT", body, event_id)


def simple_remove_event(body=None, event_id=None):
    return _simple_event("REMOVE", body, event_id)


def _simple_event(name, body=None, event_id=None):
    body = body or {
        "name": {
            "S": "CPEngineer"
        }
    }

    event_id = event_id or "f10b783edf0aba4f639df2a6eb408ee7"

    return {
        "Records": [
            {
                "eventID": event_id,
                "eventName": name,
                "eventVersion": "1.1",
                "eventSource": "aws:dynamodb",
                "awsRegion": "ap-southeast-1",
                "dynamodb": {
                    "ApproximateCreationDateTime": 1648808551.0,
                    "Keys": {
                        "name": {
                            "S": "CPEngineer"
                        }
                    },
                    "NewImage": body,
                    "SequenceNumber": "28232500000000016381400609",
                    "SizeBytes": 123,
                    "StreamViewType": "NEW_IMAGE"
                },
                "eventSourceARN": "arn:aws:dynamodb:ap-southeast-1:123456789012:table/tableName/stream/2022-03-26T16:21:38.846"
            },
        ],
    }


def simple_insert_event_multiple_records(nums, event_ids=None):
    event_ids = event_ids or [f"e{n}" for n in nums]
    assert len(nums) == len(event_ids)

    return {
        "Records": [
            {
                "eventID": event_id,
                "eventName": "INSERT",
                "eventVersion": "1.1",
                "eventSource": "aws:dynamodb",
                "awsRegion": "ap-southeast-1",
                "dynamodb": {
                    "ApproximateCreationDateTime": 1648808551.0,
                    "Keys": {
                        "name": {
                            "S": "CPEngineer",
                        },
                    },
                    "NewImage": {
                        "name": {
                            "S": "CPEngineer",
                        },
                        "num": {
                            "N": str(num),
                        },
                    },
                    "SequenceNumber": "28232500000000016381400609",
                    "SizeBytes": 123,
                    "StreamViewType": "NEW_IMAGE"
                },
                "eventSourceARN": "arn:aws:dynamodb:ap-southeast-1:123456789012:table/tableName/stream/2022-03-26T16:21:38.846"
            } for event_id, num in zip(event_ids, nums)
        ],
    }
