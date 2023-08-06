import datetime
import json
from typing import Hashable, Any

from sqlalchemy import Column, String, JSON, DateTime
from sqlalchemy import create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from wsnasa.entity.abclass.abcstorage import AbcStorage
from wsnasa.utils.makeuuid import MakeUUID
from .manifest import ObjectEncoder


Base = declarative_base()


class ModelKeyValue(Base):
    """
    Хранилище ключ-значение
    """
    __tablename__ = 'nasaapi_keyvalue'

    key = Column(String, primary_key=True, nullable=False)
    value = Column(JSON, nullable=False)
    date_create = Column(DateTime, default=datetime.datetime.now())


class StorageDatabase(AbcStorage):
    """
    Класс реализует работу с БД.
    Кэширует полученные данные
    """

    def __init__(self):
        super().__init__()
        self._connection_string = self._config.connection_string()
        self._engine = create_engine(self._connection_string)
        self._session = scoped_session(sessionmaker(autocommit=False, bind=self._engine))
        Base.metadata.create_all(bind=self._engine)

    def get(self, key: Hashable) -> Any:
        dataset = select(ModelKeyValue).where(ModelKeyValue.key == f"{MakeUUID.make(key)}")
        ret = None
        with self._engine.connect() as conn:
            for row in conn.execute(dataset).all():
                ret = json.loads(row.value)
        return ret

    def set(self, key: Hashable, value: str):
        object_encoder = ObjectEncoder()
        obj_json = object_encoder.encode(value)
        tbl = ModelKeyValue(key=MakeUUID.make(key), value=obj_json)
        self._session.add(tbl)
        self._session.commit()

    def __del__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
