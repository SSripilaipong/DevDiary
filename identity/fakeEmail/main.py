import os

import boto3
from typing import Dict


TABLE_NAME = os.environ["TABLE_NAME"]

dynamodb = boto3.client("dynamodb")


def handler(event: Dict, _):
    return {
        "SEND_CONFIRMATION_EMAIL": do_fake_send_confirmation_email,
        "READ_CONFIRMATION_EMAIL": do_fake_read_confirmation_email,
    }.get(event["command"], do_default)(event["payload"])


def do_fake_send_confirmation_email(payload: Dict):
    email = payload["email"]
    confirmation_code = payload["confirmationCode"]

    try:
        dynamodb.put_item(
            TableName=TABLE_NAME,
            Item={
                "email": {
                    "S": email,
                },
                "confirmationCode": {
                    "S": confirmation_code,
                },
            },
            ConditionExpression="attribute_not_exists(email)",
        )
    except dynamodb.exceptions.ConditionalCheckFailedException:
        return {
            "success": False,
            "message": "ConfirmationCodeAlreadySent",
        }

    return {
        "success": True,
    }


def do_fake_read_confirmation_email(payload: Dict):
    email = payload['email']

    response = dynamodb.get_item(
        TableName=TABLE_NAME,
        Key={
            "email": {
                "S": email,
            },
        },
    )

    confirmation_code = response.get("Item", {}).get("confirmationCode", None)
    if confirmation_code is None:
        return {
            "success": False,
            "message": "ConfirmationCodeNotFound",
        }

    return {
        "success": True,
        "payload": {
            "confirmationCode": confirmation_code,
        },
    }


def do_default(_):
    return {
        "success": False,
        "message": "CommandNotFound",
    }
