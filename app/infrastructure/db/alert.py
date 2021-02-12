from sqlalchemy import Column, Integer, String

from . import Base


class DbAlert(Base):
    __tablename__ = 'alerts'

    id = Column(Integer, primary_key=True)
    message = Column(String)
    time = Column(String)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'message': self.message,
            'time': self.time
        }
