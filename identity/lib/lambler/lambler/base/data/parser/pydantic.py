import json

import pydantic
from pydantic import BaseModel
from typing import Type, Any

from lambler.base.data.parser.exception import DataParsingError
from lambler.base.data.parser.parser import Parser


class PydanticParser(Parser):
    def __init__(self, model: Type[BaseModel]):
        self._model = model

    @classmethod
    def from_type(cls, type_: Type) -> 'PydanticParser':
        assert isinstance(type_, type) and issubclass(type_, BaseModel)
        return cls(type_)

    def parse(self, data: Any) -> BaseModel:
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                raise DataParsingError()

        if isinstance(data, dict):
            try:
                return self._model(**data)
            except pydantic.ValidationError:
                raise DataParsingError()
