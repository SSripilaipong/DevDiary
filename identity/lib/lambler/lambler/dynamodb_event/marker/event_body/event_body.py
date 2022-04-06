from pydantic import BaseModel
from typing import Dict, Any, Type, Optional, Callable

from lambler.base.function.input import FunctionInputSourceCollection
from lambler.base.function.marker import Marker
from lambler.dynamodb_event.input.new_image import DynamodbEventNewImageInputSource


class EventBody(Marker):
    def __init__(self):
        self._cast: Optional[Callable] = None

    def register_type(self, type_: Type):
        if type_ is dict or type_ is Dict:
            self._cast = None
        elif isinstance(type_, type) and issubclass(type_, BaseModel):
            self._cast = lambda d: type_(**d)
        else:
            raise NotImplementedError()

    def extract_param(self, data: FunctionInputSourceCollection) -> Any:
        new_image = data.of(DynamodbEventNewImageInputSource)
        data = new_image.to_dict()
        if self._cast is None:
            return data
        return self._cast(data)
