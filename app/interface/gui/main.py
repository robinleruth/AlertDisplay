import queue
import tkinter as tk
from typing import Dict

from app.domain.model.alert import Alert
from app.interface.gui.crontab_handler import CrontabHandler
from app.interface.gui.input import Input
from app.interface.gui.item import Item
from app.interface.gui.navbar import Navbar
from app.interface.gui.show_rule import ShowRule


class Main(tk.Frame):
    def __init__(self, master, in_queue: queue.Queue, out_queue: queue.Queue, cnf=None, **kw):
        if cnf is None:
            cnf = {}
        super().__init__(master, cnf, **kw)
        self.in_queue = in_queue
        self.out_queue = out_queue

        self.navbar = Navbar(self)
        self.navbar.pack(side="left", fill='y')
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill='both', expand=True)
        self.show_rule = ShowRule(self.main_frame)

        self.crontab_frame = CrontabHandler(self.main_frame)

        self.alert_frame = tk.Frame(self.main_frame)
        self.alert_frame.pack()

        self.input = Input(self.alert_frame)
        self.input.pack()

        self.items: Dict[int, Item] = {}

        self.master.after(100, self.process_queue)

    def process_queue(self):
        while not self.in_queue.empty():
            self.input.clear()
            alert: Alert = self.in_queue.get()
            if alert.id in self.items:
                self.items[alert.id].destroy()
                del self.items[alert.id]
            else:
                item = Item(self.alert_frame, alert.time, alert.message)
                self.items[alert.id] = item
                item.pack()
        self.master.after(100, self.process_queue)

    def switch_main(self, value):
        if value == 'Alerts':
            self.crontab_frame.pack_forget()
            self.show_rule.pack_forget()
            self.alert_frame.pack()
        elif value == 'CronTab':
            self.alert_frame.pack_forget()
            self.show_rule.pack_forget()
            self.crontab_frame.pack()
            self.crontab_frame.refresh()
        elif value == 'Cron rules':
            self.crontab_frame.pack_forget()
            self.alert_frame.pack_forget()
            self.show_rule.pack()
