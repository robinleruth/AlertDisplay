import os
from tkinter import *

from app.infrastructure.config import app_config


class ShowRule(Frame):
    def __init__(self, master, cnf=None, **kw):
        if cnf is None:
            cnf = {}
        super().__init__(master, cnf, **kw)

        canvas = Canvas(self, width=700, height=400)
        self.img = PhotoImage(file=os.path.join(app_config.STATIC, 'crontab.gif'))
        canvas.create_image(20, 20, anchor=NW, image=self.img)
        canvas.pack(fill='both', expand=True)
