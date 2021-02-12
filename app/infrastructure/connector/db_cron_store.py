from typing import List

from app.domain.services.cron.cron_store import CronStore
from app.infrastructure.db.cron import Cron
from app.infrastructure.db.db_session import transaction_context
from app.infrastructure.log import logger


class DbCronStore(CronStore):
    def is_cron(self, message: str) -> bool:
        with transaction_context() as session:
            r = session.query(Cron).filter_by(message=message).all()
            if len(r) == 0:
                return False
            else:
                return True

    def get_all(self) -> List[Cron]:
        with transaction_context() as session:
            r = session.query(Cron).all()
        return r

    def remove_one(self, _id: int):
        with transaction_context() as session:
            r = session.query(Cron).filter_by(id=_id).first()
            logger.info('Removing cron {}'.format(r.serialize))
            session.delete(r)

    def put(self, message: str, cron: str) -> Cron:
        with transaction_context() as session:
            entry = Cron(message=message, cron=cron)
            session.add(entry)
            session.commit()
            logger.info('Cron added {}'.format(entry))
        return entry

    def get_one(self, message: str) -> str:
        with transaction_context() as session:
            result: Cron = session.query(Cron).filter_by(message=message).first()
            result = result.serialize
        return result


