from tkinter import *
from typing import Dict

from app.domain.services.cron.cron_service import CronService
from app.interface.gui.cron_item import CronItem


class CrontabHandler(Frame):
    cron_service: CronService

    def __init__(self, master, cnf=None, **kw):
        if cnf is None:
            cnf = {}
        super().__init__(master, cnf, **kw)
        self.cron_service = CronService()
        self.items: Dict[int, CronItem] = {}
        CronItem(self, "Id", "Cron", "Message", title=True).pack()

    def refresh(self):
        lst = self.cron_service.get_all()
        for cron in lst:
            if cron.id not in self.items:
                item = CronItem(self, cron.id, cron.cron, cron.message)
                self.items[cron.id] = item
                item.pack()

    def remove_from_dict(self, _id):
        del self.items[_id]
