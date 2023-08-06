from typing import List

from wsnasa.entity.manifest import Photo, DayOfMars, Manifest
from wsnasa.utils.repo import Repo


class ABCRover:
    """
    Родительский класс марсохода
    """

    def __init__(self, rover: str):
        self.__name = rover
        self._base_uri = f'https://api.nasa.gov/mars-photos/api/v1/'
        self.__manifest = Repo.manifest(self.__name)

    def manifest(self) -> Manifest:
        """
        Возвращает манифест марсохода.
        """
        return self.__manifest

    def photos(self, days: DayOfMars) -> List[Photo]:
        """
        Возвращает массив классов Photo за выбранный день
        """
        return Repo.photos(self.__manifest, days)

    def __str__(self) -> str:
        return self.__name
