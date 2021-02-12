import abc
import datetime as dt


class IParser(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def parse(self, time: str) -> dt.datetime:
        pass
