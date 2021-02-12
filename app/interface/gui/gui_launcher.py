from queue import Queue
from threading import Thread
from tkinter import Tk

from app.interface.gui.main import Main


class GuiLauncher(Thread):
    def __init__(self, in_queue: Queue, out_queue: Queue) -> None:
        super().__init__()
        self.daemon = True
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self) -> None:
        root = Tk(baseName="Alerts")
        Main(root, self.in_queue, self.out_queue).pack(side='top', fill='both', expand=True)
        root.mainloop()
