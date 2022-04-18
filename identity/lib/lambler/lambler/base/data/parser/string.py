from typing import Type, Any

from lambler.base.data.parser.parser import Parser


class StringParser(Parser):
    @classmethod
    def from_type(cls, type_: Type) -> 'StringParser':
        assert type_ is str
        return cls()

    def parse(self, data: Any) -> str:
        return str(data)
