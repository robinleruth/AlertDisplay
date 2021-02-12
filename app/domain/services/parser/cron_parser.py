import datetime as dt

from app.domain.services.crontab import CronTab
from app.domain.services.parser.i_parser import IParser


class CronParser(IParser):
    def parse(self, message: str, now=None) -> dt.datetime:
        if now is None:
            now = dt.datetime.now()
        crontab = CronTab(message)
        seconds = crontab.next(now)
        return now + dt.timedelta(seconds=seconds)
