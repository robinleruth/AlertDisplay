from abc import ABCMeta, abstractmethod
from typing import List

from app.domain.model.alert import Alert


class TaskStore(metaclass=ABCMeta):
    @abstractmethod
    def get_all(self) -> List[Alert]:
        pass

    @abstractmethod
    def remove_one(self, _id: int):
        pass

    @abstractmethod
    def put(self, alert: Alert) -> Alert:
        pass

    @abstractmethod
    def alert_is_in_db(self, message: str, time: str) -> bool:
        pass
