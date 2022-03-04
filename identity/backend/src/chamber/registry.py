from typing import Optional

from chamber.message.bus import MessageBus


class ChamberRegistryMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(ChamberRegistryMeta, cls).__call__(*args, **kwargs)
        else:
            assert not args and not kwargs
        return cls._instances[cls]


class ChamberRegistry(metaclass=ChamberRegistryMeta):
    def __init__(self):
        self._message_bus: Optional[MessageBus] = None

    @property
    def message_bus(self) -> MessageBus:
        return self._message_bus

    @message_bus.setter
    def message_bus(self, obj: MessageBus):
        self._message_bus = obj
        if obj is not None:
            self._on_message_bus_attached()

    def _on_message_bus_attached(self):
        pass
