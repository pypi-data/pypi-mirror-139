from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class RequestAPOD:
    """
    Содержит данные запроса o Astronomy Picture of the Day.
    """
    date: datetime = field(default=datetime.today().strftime('%Y-%m-%d'))
    start_date: datetime = field(default=None)
    end_date: datetime = field(default=datetime.today().strftime('%Y-%m-%d'))
    count: int = field(default=None)
    thumbs: bool = field(default=False)
    api_key: str = field(default=None)


@dataclass
class ResponseAPOD:
    """
    Содержит данные ответа o Astronomy Picture of the Day.
    """
    title: str = field(default=None)
    explanation: str = field(default=None)
    hdurl: str = field(default=None)
    url: str = field(default=None)
    date: datetime = field(default=None)
    copyright: str = field(default=None)
    media_type: str = field(default=None)
    service_version: str = field(default=None)
