from typing import Dict, List, Type

from lambda_handler.mapper.exception import NoServiceEventMatchedException
from lambda_handler.service_event.abstract import ServiceEvent


class ServiceEventMapper:
    def __init__(self, event_types: List[Type[ServiceEvent]]):
        self._event_types = event_types

    def map(self, raw_event: Dict) -> ServiceEvent:
        for event_type in self._event_types:
            if event_type.match(raw_event):
                return event_type.from_raw_event(raw_event)
        raise NoServiceEventMatchedException()

    @classmethod
    def from_list(cls, event_types: List[Type[ServiceEvent]]) -> 'ServiceEventMapper':
        return cls(event_types)
