from abc import abstractmethod, ABC


class SecretManager(ABC):
    @abstractmethod
    def get_private_key(self) -> bytes:
        pass

    @abstractmethod
    def get_public_key(self) -> bytes:
        pass
