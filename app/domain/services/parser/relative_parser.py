import datetime as dt
from collections import namedtuple

from app.domain.services.parser.i_parser import IParser

RelativeTime = namedtuple("RelativeTime", ["hours", "minutes", "seconds"])


class RelativeParser(IParser):
    def __init__(self):
        self.now = None

    def parse(self, time: str, now=None) -> dt.datetime:
        if now is None:
            self.now = dt.datetime.now()
        else:
            self.now = now
        r = self._parse(time)
        return self.now + dt.timedelta(hours=r.hours, minutes=r.minutes, seconds=r.seconds)

    def _parse(self, time: str) -> RelativeTime:
        hours = 0
        minutes = 0
        seconds = 0
        lst = time.split("h")
        if len(lst) == 2:
            hours = int(lst[0])
            time = lst[1]
        lst = time.split("m")
        if len(lst) == 2:
            minutes = int(lst[0])
            time = lst[1]
        lst = time.split("s")
        if len(lst) == 2:
            seconds = int(lst[0])
        return RelativeTime(hours=hours, minutes=minutes, seconds=seconds)
