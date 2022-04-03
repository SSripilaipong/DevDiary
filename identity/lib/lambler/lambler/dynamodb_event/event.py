from typing import List, Dict, Optional

from pydantic import BaseModel, Field

from lambler.base.event import LamblerEvent


class Data(BaseModel):
    approximate_creation_date_time: float = Field(alias="ApproximateCreationDateTime")
    keys: Dict = Field(alias="Keys")
    new_image: Optional[Dict] = Field(alias="NewImage", default=None)
    sequence_number: str = Field(alias="SequenceNumber")
    size_bytes: int = Field(alias="SizeBytes")
    stream_view_type: str = Field(alias="StreamViewType")


class DynamodbEvent(BaseModel, LamblerEvent):
    event_id: str = Field(alias="eventID")
    event_name: str = Field(alias="eventName")
    event_version: str = Field(alias="eventVersion")
    event_source: str = Field(alias="eventSource")
    aws_region: str = Field(alias="awsRegion")
    event_source_arn: str = Field(alias="eventSourceARN")
    dynamodb: Data
