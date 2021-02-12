from tkinter import *
from threading import Thread

from app.domain.model.alert import Alert


class AlertWindow(Thread):
    def __init__(self, alert: Alert):
        super().__init__()
        self.daemon = True
        self.alert: Alert = alert

    def run(self) -> None:
        root = Tk()
        Label(root, text=self.alert.message).pack()
        root.mainloop()
