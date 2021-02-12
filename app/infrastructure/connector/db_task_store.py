from dataclasses import asdict
from typing import List

from app.domain.model.alert import Alert
from app.domain.services.task_store import TaskStore
from app.infrastructure.db.alert import DbAlert
from app.infrastructure.db.db_session import transaction_context
from app.infrastructure.log import logger


class DbTaskStore(TaskStore):
    def get_all(self) -> List[Alert]:
        with transaction_context() as session:
            r = session.query(DbAlert).all()
            r = list(map(lambda x: Alert(**x.serialize), r))
        return r

    def remove_one(self, _id: int):
        with transaction_context() as session:
            r = session.query(DbAlert).filter_by(id=_id).first()
            logger.info('Removing alert {}'.format(r.serialize))
            session.delete(r)

    def put(self, alert: Alert) -> Alert:
        with transaction_context() as session:
            entry = DbAlert(**asdict(alert))
            session.add(entry)
            session.commit()
            alert = Alert(**entry.serialize)
            logger.info('Alert added in DB : {}'.format(alert))
        return alert

    def alert_is_in_db(self, message: str, time: str) -> bool:
        with transaction_context() as session:
            r = session.query(DbAlert).filter_by(message=message).filter_by(time=time).all()
            if len(r) == 0:
                return False
            else:
                return True



