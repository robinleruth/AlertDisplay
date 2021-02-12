from abc import ABCMeta, abstractmethod
from typing import List

from app.infrastructure.db.cron import Cron


class CronStore(metaclass=ABCMeta):
    @abstractmethod
    def get_all(self) -> List[Cron]:
        pass

    @abstractmethod
    def remove_one(self, _id: int):
        pass

    @abstractmethod
    def put(self, message: str, cron: str) -> Cron:
        pass

    @abstractmethod
    def is_cron(self, message: str) -> bool:
        pass

    @abstractmethod
    def get_one(self, message: str):
        pass
