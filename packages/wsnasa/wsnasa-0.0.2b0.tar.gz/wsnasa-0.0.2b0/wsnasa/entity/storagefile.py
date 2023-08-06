from .manifest import DayOfMars, Photo
from typing import List, Tuple
import os

from wsnasa.entity.abclass.abcstorage import AbcStorage


class StorageFile(AbcStorage):

    def __init__(self):
        super().__init__()
        self.__path = '{}/{}'
        self.__cache = {}

    def get(self, day: DayOfMars) -> List[DayOfMars]:
        return self.__cache.get(day, None)

    def set(self, day: DayOfMars, data: Tuple[Photo]):
        for i in data:
            print(f'/home/pi/petprojects/nasaapi/nasaapi/Curiosity/{i.id}.jpg')
            with open(f'/home/pi/petprojects/nasaapi/nasaapi/Curiosity/{i.id}.jpg', 'wb') as f:
                f.write(i.download())

