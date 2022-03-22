from contextlib import contextmanager


class FieldController:
    def __init__(self):
        self._can_read = False
        self._can_write = False

    @contextmanager
    def allow_read(self):
        self._can_read = True
        try:
            yield
        finally:
            self._can_read = False

    @contextmanager
    def allow_read_write(self):
        self._can_read = True
        self._can_write = True
        try:
            yield
        finally:
            self._can_read = False
            self._can_write = False

    @property
    def can_read(self) -> bool:
        return self._can_read

    @property
    def can_write(self) -> bool:
        return self._can_write
