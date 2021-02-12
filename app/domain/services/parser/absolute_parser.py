import datetime as dt

from app.domain.services.parser.i_parser import IParser


class AbsoluteParser(IParser):
    def parse(self, time: str) -> dt.datetime:
        return dt.datetime.strptime(time, '%Y-%m-%d %H:%M')
