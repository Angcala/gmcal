from enum import Enum
from datetime import datetime


class Response(Enum):
    YES = "yes"
    NO = "no"
    COUNTER = "new time proposal"

    suggested_time: datetime | None = None

    @classmethod
    def set_suggested_time(cls, new_time: datetime):
        cls.suggested_time = new_time


