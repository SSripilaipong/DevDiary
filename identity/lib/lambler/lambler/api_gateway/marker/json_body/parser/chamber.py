from typing import Dict, Type

from chamber.data.model import DataModel
from chamber.data.exception import DeserializationFailedException
from lambler.api_gateway.exception import InvalidParameterError
from lambler.api_gateway.marker.json_body.parser.parser import Parser


class ChamberParser(Parser):
    def __init__(self, model: Type[DataModel]):
        self._model = model

    @classmethod
    def from_type(cls, type_: Type) -> 'ChamberParser':
        assert isinstance(type_, type) and issubclass(type_, DataModel)
        return cls(type_)

    def parse(self, data: Dict) -> DataModel:
        assert isinstance(data, dict)

        try:
            return self._model.from_dict(data)
        except DeserializationFailedException:
            raise InvalidParameterError()
