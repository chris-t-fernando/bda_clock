from typing import List

# from datetime
import datetime

from pydantic import BaseModel


class NewClock(BaseModel):
    interval: int
    start: datetime.datetime
    id: str
    tz: str


class Clock(NewClock):
    now: datetime.datetime


class Clocks(BaseModel):
    clocks: List[Clock]
