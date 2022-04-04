import pydantic
from pydantic import BaseModel
from typing import Type, Optional, Dict, Any

import chamber.data.exception
from chamber.data.model import DataModel
from lambler.api_gateway.endpoint.exception import InvalidParameterError
from lambler.base.marker import Marker


class JSONBody(Marker):
    def __init__(self):
        self._type: Optional[Type] = None

    def register_type(self, type_: Type):
        if type_ is dict or type_ is Dict:
            self._type = dict
        elif isinstance(type_, type) and issubclass(type_, BaseModel):
            self._type = type_
        elif isinstance(type_, type) and issubclass(type_, DataModel):
            self._type = type_
        else:
            raise NotImplementedError()  # TODO: implement this

    def extract_param(self, data: Dict) -> Any:
        if self._type is dict:
            return data
        elif isinstance(self._type, type) and issubclass(self._type, BaseModel):
            try:
                return self._type(**data)
            except pydantic.ValidationError:
                raise InvalidParameterError()
        elif isinstance(self._type, type) and issubclass(self._type, DataModel):
            try:
                return self._type.from_dict(data)
            except chamber.data.exception.DeserializationFailedException:
                raise InvalidParameterError()
        else:
            raise NotImplementedError()
