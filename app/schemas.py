from typing import List

from pydantic import BaseModel


class NewClock(BaseModel):
    interval: int
    start: str
    id: str


class Clock(NewClock):
    now: str


class Clocks(BaseModel):
    clocks: List[Clock]
