import os

import json

from domain.identity.email.exception import ConfirmationEmailNotFoundException
from domain.identity.email.service import EmailService
from domain.identity.value_object.email import Email


FAKE_EMAIL_LAMBDA_NAME = os.environ.get("FAKE_EMAIL_LAMBDA_NAME", "")


try:
    import boto3
    import botocore.response
except ImportError:
    boto3 = None
    botocore = None


class EmailServiceInMemory(EmailService):
    def __init__(self):
        self.lambda_client = boto3.client('lambda') if boto3 is not None else None

    def send_confirmation_email(self, email: Email, confirmation_code: str):
        assert self.lambda_client

        payload = {
            "command": "SEND_CONFIRMATION_EMAIL",
            "payload": {
                "email": email,
                "confirmationCode": confirmation_code,
            },
        }

        response: botocore.response.StreamingBody = self.lambda_client.invoke(
            FunctionName=FAKE_EMAIL_LAMBDA_NAME,
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        ).get('Payload', None)

        assert response is not None
        assert json.loads(response.read()).get('success', False)

    def get_latest_confirmation_code(self, email: Email) -> str:
        assert self.lambda_client

        payload = {
            "command": "READ_CONFIRMATION_EMAIL",
            "payload": {
                "email": email,
            },
        }

        response: botocore.response.StreamingBody = self.lambda_client.invoke(
            FunctionName=FAKE_EMAIL_LAMBDA_NAME,
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        ).get('Payload', None)

        assert response is not None

        payload = json.loads(response.read())
        if not payload.get('success', False):
            raise ConfirmationEmailNotFoundException()

        confirmation_code = payload.get('confirmationCode', None)
        assert confirmation_code is not None
        return confirmation_code
