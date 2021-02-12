import datetime as dt
from typing import List

from app.domain.services.cron.cron_store import CronStore
from app.domain.services.crontab import CronTab
from app.domain.services.parser.cron_parser import CronParser
from app.infrastructure.connector.db_cron_store import DbCronStore
from app.infrastructure.db.cron import Cron


class CronService:
    cron_store: CronStore
    cron_parser: CronParser

    def __init__(self):
        self.cron_store = DbCronStore()
        self.cron_parser = CronParser()

    def get_all(self) -> List[Cron]:
        return self.cron_store.get_all()

    def remove_one(self, _id: int):
        self.cron_store.remove_one(_id)

    def put(self, message: str, cron: str) -> Cron:
        return self.cron_store.put(message, cron)

    def cron_in_db(self, message: str) -> bool:
        return self.cron_store.is_cron(message)

    @staticmethod
    def is_cron(time: str) -> bool:
        try:
            c = CronTab(time)
            # c.next()
            return True
        except ValueError:
            return False

    def get_next_time(self, message) -> dt.datetime:
        cron = self.cron_store.get_one(message)
        return self.cron_parser.parse(cron['cron'])
