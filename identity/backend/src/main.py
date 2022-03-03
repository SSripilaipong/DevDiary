import json
from lambda_event.api_gateway import RawApiGatewayEvent


def handler(event, context):
    print('context:', context)
    print('event:', event)
    print(RawApiGatewayEvent(event))
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps({
            "message": "OK!",
        }),
    }
