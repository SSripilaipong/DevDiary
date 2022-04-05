import pydantic
from typing import Dict, Type, Optional

from lambler.api_gateway.aws.event.event import AWSAPIGatewayEvent
from lambler.api_gateway.aws.event.event_v2 import AWSAPIGatewayEventV2
from lambler.api_gateway.aws.event.version import AWSEventVersion
from lambler.api_gateway.event import APIGatewayEvent


class AWSEventParser:
    def __init__(self):
        self._models: Dict[AWSEventVersion, Type[AWSAPIGatewayEvent]] = {}

    def register_version(self, version: AWSEventVersion, model: Type[AWSAPIGatewayEvent]):
        self._models[version] = model

    def parse(self, event: Dict, version: AWSEventVersion) -> Optional[APIGatewayEvent]:
        if version is None:
            try:
                return APIGatewayEvent(**event)
            except pydantic.ValidationError:
                return None

        model = self._models.get(version)
        if model is None:
            raise NotImplementedError()

        return model.from_dict(event).normalize()


event_parser = AWSEventParser()
event_parser.register_version(AWSEventVersion.V2, AWSAPIGatewayEventV2)
