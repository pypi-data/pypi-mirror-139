from abc import ABC, abstractmethod
from typing import Hashable, Any

from wsnasa.config import Config


class AbcStorage(ABC):
    """
    Интерфейс хранилища
    """
    def __init__(self):
        self._config = Config()

    @abstractmethod
    def get(self, key: Hashable) -> Any:
        raise NotImplementedError

    @abstractmethod
    def set(self, key: Hashable, value: Any):
        raise NotImplementedError
