import asyncio
import datetime as dt
import queue
from typing import List

from app.domain.model.alert import Alert
from app.domain.services.cron.cron_service import CronService
from app.domain.services.parser.parser import Parser
from app.domain.services.task_store import TaskStore
from app.infrastructure.config import app_config
from app.infrastructure.connector.db_task_store import DbTaskStore
from app.infrastructure.db import Cron
from app.infrastructure.log import logger
from app.interface.gui.alert_window import AlertWindow


class TaskService:
    sync_queue: queue.Queue
    async_queue: asyncio.Queue
    pending: asyncio.Queue
    parser: Parser
    task_store: TaskStore
    cron_service: CronService

    def __init__(self, q, aq) -> None:
        self.sync_queue = q
        self.async_queue = aq
        self.pending = asyncio.Queue()
        self.parser = Parser()
        self.loop = asyncio.get_event_loop()
        self.task_store = DbTaskStore()
        self.cron_service = CronService()

        self.loop.create_task(self.schedule_all_from_db())

    async def wait(self):
        logger.info("waiting for messages in queue")
        message = await self.async_queue.get()
        logger.info("Message received : {}".format(message))
        await self.pending.put(message)

    def create_alert(self, time: dt.datetime, message: str):
        alert: Alert = Alert(None, message, time.strftime(app_config.TIME_FORMAT))
        alert = self.task_store.put(alert)
        logger.info("Creating alert {}".format(alert))
        self.sync_queue.put(alert)
        self.loop.create_task(
            self.run_at(dt.datetime.strptime(alert.time, app_config.TIME_FORMAT), self.display_alert(alert)))

    async def process_messages(self):
        logger.info("processing messages : {}".format(self.pending.qsize()))
        while not self.pending.empty():
            r = await self.pending.get()
            if self.cron_service.is_cron(r[0]):
                self.cron_service.put(r[1], r[0])
            time = self.parser.parse(r[0])
            self.create_alert(time, r[1])
            # alert: Alert = Alert(None, r[1], time.strftime('%Y-%m-%d %H-%M-%S'))
            # alert = self.task_store.put(alert)
            # self.sync_queue.put(alert)
            # self.loop.create_task(
            #     self.run_at(dt.datetime.strptime(alert.time, '%Y-%m-%d %H-%M-%S'), self.display_alert(alert)))

    @staticmethod
    async def wait_until(d: dt.datetime):
        now = dt.datetime.now()
        await asyncio.sleep((d - now).total_seconds())

    async def run_at(self, d: dt.datetime, coro):
        await self.wait_until(d)
        return await coro

    async def display_alert(self, alert: Alert):
        logger.info('Displaying alert'.format(alert))
        # remove from db
        self.task_store.remove_one(alert.id)
        # send message to queue to remove it from main ui
        self.sync_queue.put(alert)
        # start gui for Alert
        AlertWindow(alert).start()
        if self.cron_service.cron_in_db(alert.message):
            logger.info("Alert is cron, rescheduling")
            time = self.cron_service.get_next_time(alert.message)
            self.create_alert(time, alert.message)

    async def schedule_all_from_db(self):
        alerts = self.task_store.get_all()
        for alert in alerts:
            self.sync_queue.put(alert)
            if dt.datetime.strptime(alert.time, app_config.TIME_FORMAT) < dt.datetime.now():
                await self.display_alert(alert)
            else:
                self.loop.create_task(
                    self.run_at(dt.datetime.strptime(alert.time, app_config.TIME_FORMAT), self.display_alert(alert)))

        crons: List[Cron] = self.cron_service.get_all()
        for cron in crons:
            time = self.cron_service.get_next_time(cron.message)
            if not self.task_store.alert_is_in_db(cron.message, time.strftime(app_config.TIME_FORMAT)):
                self.create_alert(time, cron.message)
            else:
                logger.info("Alert already in db : {} - {}".format(cron.message, time.strftime(app_config.TIME_FORMAT)))
