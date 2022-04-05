from typing import Dict, Any, Type, Optional

from lambler.base.function.marker import Marker


class EventBody(Marker):
    def __init__(self):
        self._type: Optional[Type] = None

    def register_type(self, type_: Type):
        if type_ is dict or type_ is Dict:
            self._type = type_
        else:
            raise NotImplementedError()

    def extract_param(self, data: Dict) -> Any:
        if isinstance(data, dict):
            return data
        raise NotImplementedError()
