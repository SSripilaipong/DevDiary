def simple_notification_event(topic_name=None, message=None):
    topic_name = topic_name or "sns-lambda"
    message = message or "Hello from SNS!"

    return {
        "Records": [
            {
                "EventVersion": "1.0",
                "EventSubscriptionArn": f"arn:aws:sns:ap-southeast-2:123456789012:{topic_name}:21be56ed-a058-49f5-8c98-aedd2564c486",
                "EventSource": "aws:sns",
                "Sns": {
                    "SignatureVersion": "1",
                    "Timestamp": "2019-01-02T12:45:07.000Z",
                    "Signature": "tcc6faL2yUC6dgZdmrwh1Y4cGa/ebXEkAi6RibDsvpi+tE/1+82j...65r==",
                    "SigningCertUrl": "https://sns.ap-southeast-2.amazonaws.com/SimpleNotificationService-ac565b8b1a6c5d002d285f9598aa1d9b.pem",
                    "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
                    "Message": message,
                    "MessageAttributes": {
                        "Test": {
                            "Type": "String",
                            "Value": "TestString"
                        },
                        "TestBinary": {
                            "Type": "Binary",
                            "Value": "TestBinary"
                        }
                    },
                    "Type": "Notification",
                    "UnsubscribeUrl": "https://sns.ap-southeast-2.amazonaws.com/?Action=Unsubscribe&amp;SubscriptionArn=arn:aws:sns:ap-southeast-2:123456789012:test-lambda:21be56ed-a058-49f5-8c98-aedd2564c486",
                    "TopicArn": f"arn:aws:sns:ap-southeast-2:123456789012:{topic_name}",
                }
            }
        ]
    }
