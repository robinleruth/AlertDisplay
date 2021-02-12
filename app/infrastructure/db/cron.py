from sqlalchemy import Column, Integer, String

from . import Base


class Cron(Base):
    __tablename__ = 'cron'

    id = Column(Integer, primary_key=True)
    message = Column(String)
    cron = Column(String)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'message': self.message,
            'cron': self.cron
        }
