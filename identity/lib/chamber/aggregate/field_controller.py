from contextlib import contextmanager


class FieldController:
    def __init__(self):
        self._can_read = False

    @contextmanager
    def allow_read(self):
        self._can_read = True
        try:
            yield
        finally:
            self._can_read = False

    @property
    def can_read(self) -> bool:
        return self._can_read
