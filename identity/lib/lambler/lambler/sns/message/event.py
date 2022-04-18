from typing import List, Dict, Any

from pydantic import BaseModel, Field

from lambler.base.event import LamblerEvent


class SNSMessageEventRecordNotification(BaseModel):
    signature_version: str = Field(alias="SignatureVersion")
    timestamp: str = Field(alias="Timestamp")
    signature: str = Field(alias="Signature")
    signing_cert_url: str = Field(alias="SigningCertUrl")
    message_id: str = Field(alias="MessageId")
    message: str = Field(alias="Message")
    message_attributes: Dict[str, Dict[str, Any]] = Field(alias="MessageAttributes")
    type_: str = Field(alias="Type")
    unsubscribe_url: str = Field(alias="UnsubscribeUrl")
    topic_arn: str = Field(alias="TopicArn")
    subject: str = Field(alias="Subject")


class SNSMessageEventRecord(BaseModel):
    event_version: str = Field(alias="EventVersion")
    event_subscription_arn: str = Field(alias="EventSubscriptionArn")
    event_source: str = Field(alias="EventSource")
    sns: SNSMessageEventRecordNotification = Field(alias="Sns")


class SNSMessageEvent(BaseModel, LamblerEvent):
    records: List[SNSMessageEventRecord] = Field(alias="Records")
