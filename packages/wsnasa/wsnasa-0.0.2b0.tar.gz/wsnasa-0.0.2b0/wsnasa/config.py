from typing import Any


class Config:
    """
    Хранит необходимые настройки
    """
    __instance = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls.__instance:
            cls.__token = kwargs.get('token', None)
            cls.__base_uri = kwargs.get('base_uri', 'https://api.nasa.gov/mars-photos/api/v1/')
            cls.__connection_string = kwargs.get('connection_string', None)
            cls.__storage = kwargs.get('storage', None)
            if cls.__token is None:
                raise Exception('Не указан токен')

            if cls.__storage is None:
                raise Exception('Не указано хранилище')

            cls.__instance[cls] = cls
        return cls.__instance[cls]

    @classmethod
    def token(cls) -> str:
        return cls.__token

    @classmethod
    def base_uri(cls) -> str:
        return cls.__base_uri

    @classmethod
    def connection_string(cls) -> str:
        return cls.__connection_string

    @classmethod
    def storage(cls) -> Any:
        return cls.__storage()
