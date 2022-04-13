from typing import Callable

from datetime import datetime
from collections import OrderedDict
import json
import logging


class LogFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()

        self._now: Callable[[], datetime] = datetime.now

    def format(self, record) -> str:
        message = OrderedDict()

        now: datetime = self._now()
        message["datetime"] = now.strftime("%Y-%m-%d %H:%M:%S.%f")

        message.update(OrderedDict(record.msg))
        message["timestamp"] = now.timestamp()

        return json.dumps(message, default=str)


log_handler = logging.StreamHandler()
log_handler.setFormatter(LogFormatter())
log_handler.setLevel(logging.DEBUG)
logger = logging.getLogger("lambler")
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)

