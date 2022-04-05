from typing import Type, TypeVar, Dict

from abc import ABC, abstractmethod

from lambler.api_gateway.event import APIGatewayEvent


T = TypeVar("T", bound="AWSAPIGatewayEvent")


class AWSAPIGatewayEvent(ABC):
    @abstractmethod
    def normalize(self) -> APIGatewayEvent:
        pass

    @classmethod
    @abstractmethod
    def from_api_event(cls: Type[T], event: APIGatewayEvent) -> T:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls: Type[T], event: Dict) -> T:
        pass
