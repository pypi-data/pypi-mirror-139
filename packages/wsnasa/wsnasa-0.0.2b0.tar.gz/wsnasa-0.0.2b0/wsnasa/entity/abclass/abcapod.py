import datetime
import random
from typing import Tuple
from wsnasa.utils.repo import Repo, ResponseAPOD


class AbcAPOD:

    def __init__(self):
        self._base_uri = f'https://api.nasa.gov/planetary/apod'
        self._start_date = datetime.date(year=1995, month=6, day=16)  #ограничение сервиса
        self._end_date = datetime.date.today()
        self.__name = 'APOD'
        self._repo = Repo

    def get_random(self) -> ResponseAPOD:
        rand = random.randint(1, abs((self._end_date - self._start_date).days))
        rand_day = self._start_date + datetime.timedelta(days=rand)
        return self._repo.apod(rand_day)

    def get_today(self) -> ResponseAPOD:
        return self._repo.apod(datetime.date.today())

    def get_list(self, start_date: datetime, end_date: datetime) -> Tuple[ResponseAPOD]:
        return self._repo.apod_list(start_date=start_date, end_date=end_date)

    def __str__(self) -> str:
        return self.__name
