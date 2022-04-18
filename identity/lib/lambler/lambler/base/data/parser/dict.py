import json

from typing import Dict, Type

from lambler.base.data.parser.exception import DataParsingError
from lambler.base.data.parser.parser import Parser


class DictParser(Parser):
    @classmethod
    def from_type(cls, type_: Type) -> 'DictParser':
        assert type_ is Dict or type_ is dict
        return cls()

    def parse(self, data: Dict) -> Dict:
        if isinstance(data, dict):
            return data
        elif isinstance(data, str):
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                raise DataParsingError()

        raise NotImplementedError()
