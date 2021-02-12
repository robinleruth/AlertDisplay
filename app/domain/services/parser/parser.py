import datetime as dt
from typing import Set

from app.domain.services.parser.absolute_parser import AbsoluteParser
from app.domain.services.parser.cron_parser import CronParser
from app.domain.services.parser.i_parser import IParser
from app.domain.services.parser.relative_parser import RelativeParser
from app.infrastructure.log import logger


class Parser(IParser):
    def __init__(self):
        self.parsers: Set[IParser] = {CronParser(), RelativeParser(), AbsoluteParser()}

    def parse(self, time: str) -> dt.datetime:
        for parser in self.parsers:
            try:
                return parser.parse(time)
            except Exception as e:
                logger.info("Message {} couldn't be parsed with parser {}".format(time, parser.__class__.__name__))

        raise Exception("Couldn't parse message {}", time)
