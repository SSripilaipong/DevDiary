def simple_insert_event():

    return {
        "Records": [
            {
                "eventID": "f10b783edf0aba4f639df2a6eb408ee7",
                "eventName": "INSERT",
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
                    "NewImage": {
                        "name": {
                            "S": "CPEngineer"
                        }
                    },
                    "SequenceNumber": "28232500000000016381400609",
                    "SizeBytes": 123,
                    "StreamViewType": "NEW_IMAGE"
                },
                "eventSourceARN": "arn:aws:dynamodb:ap-southeast-1:123456789012:table/tableName/stream/2022-03-26T16:21:38.846"
            },
        ],
    }
