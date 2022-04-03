from enum import Enum


class DynamodbEventType(str, Enum):
    INSERT = "INSERT"
