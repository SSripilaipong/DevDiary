import json

from typing import Type, Any

from chamber.data.model import DataModel
from chamber.data.exception import DeserializationFailedException
from lambler.base.data.parser.exception import DataParsingError
from lambler.base.data.parser.parser import Parser


class ChamberParser(Parser):
    def __init__(self, model: Type[DataModel]):
        self._model = model

    @classmethod
    def from_type(cls, type_: Type) -> 'ChamberParser':
        assert isinstance(type_, type) and issubclass(type_, DataModel)
        return cls(type_)

    def parse(self, data: Any) -> DataModel:
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except:
                raise NotImplementedError()

        if isinstance(data, dict):
            try:
                return self._model.from_dict(data)
            except DeserializationFailedException:
                raise DataParsingError()
