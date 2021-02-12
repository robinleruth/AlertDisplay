from tkinter import *

from app.domain.services.cron.cron_service import CronService


class CronItem(Frame):
    cron_service: CronService

    def __init__(self, master, id, time: str, message: str, title: bool = False, cnf=None, **kw):
        if cnf is None:
            cnf = {}
        super().__init__(master, cnf, **kw)
        self.cron_service = CronService()

        self.id = id
        self.time = time
        self.message = message

        Label(self, text=self.id).grid(row=0, column=0)
        Label(self, text=self.time).grid(row=0, column=2)
        Label(self, text=self.message).grid(row=0, column=4)
        if not title:
            Button(self, text="Delete", command=self.delete).grid(row=0, column=6)

    def delete(self):
        self.cron_service.remove_one(self.id)
        self.master.remove_from_dict(self.id)
        self.destroy()
