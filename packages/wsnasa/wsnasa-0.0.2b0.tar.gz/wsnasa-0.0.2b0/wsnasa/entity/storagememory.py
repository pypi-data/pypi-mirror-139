from typing import List, Tuple

from wsnasa.entity.abclass.abcstorage import AbcStorage
from .manifest import DayOfMars, Photo


class StorageMemory(AbcStorage):
    """
    Кэширует полученные данные в памяти
    """

    def __init__(self):
        super().__init__()
        self.__cache = {}

    def get(self, day: DayOfMars) -> List[DayOfMars]:
        return self.__cache.get(day, None)

    def set(self, day: DayOfMars, data: Tuple[Photo]):
        self.__cache.setdefault(day, data)
