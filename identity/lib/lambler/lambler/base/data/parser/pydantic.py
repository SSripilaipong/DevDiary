import pydantic
from pydantic import BaseModel
from typing import Dict, Type

from lambler.base.data.parser.exception import DataParsingError
from lambler.base.data.parser.parser import Parser


class PydanticParser(Parser):
    def __init__(self, model: Type[BaseModel]):
        self._model = model

    @classmethod
    def from_type(cls, type_: Type) -> 'PydanticParser':
        assert isinstance(type_, type) and issubclass(type_, BaseModel)
        return cls(type_)

    def parse(self, data: Dict) -> BaseModel:
        assert isinstance(data, dict)
        try:
            return self._model(**data)
        except pydantic.ValidationError:
            raise DataParsingError()
