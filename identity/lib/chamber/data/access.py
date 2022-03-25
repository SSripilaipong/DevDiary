class AccessController:
    def __init__(self):
        self.__can_read = False

    def can_read(self) -> bool:
        return self.__can_read
