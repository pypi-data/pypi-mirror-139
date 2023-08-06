import uuid
from typing import Iterable


class MakeUUID:
    """
    Класс для генерации UID
    """
    @staticmethod
    def make(key) -> uuid.UUID:
        key_str = key
        if isinstance(key, uuid.UUID):
            return key

        if hasattr(key, 'uuid'):
            return key.uuid()

        if isinstance(key, Iterable):
            key_str = ''.join([str(i) for i in key])

        return uuid.uuid3(uuid.NAMESPACE_URL, key_str)
