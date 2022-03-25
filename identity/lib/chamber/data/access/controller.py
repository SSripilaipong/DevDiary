class AccessController:
    def __init__(self):
        self.__can_read = False
        self.__can_write = False

    def can_read(self) -> bool:
        return self.__can_read

    def allow_read(self):
        self.__can_read = True

    def prevent_read(self):
        self.__can_read = False

    def can_write(self) -> bool:
        return self.__can_write

    def allow_read_write(self):
        self.__can_read = True
        self.__can_write = True

    def prevent_read_write(self):
        self.__can_read = False
        self.__can_write = False
