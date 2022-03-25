from typing import Dict

from chamber.data.model import DataModel


class Message(DataModel):
    def to_dict(self) -> Dict:
        return {
            'name': self.__class__.__name__,
            'body': super().to_dict(),
        }
