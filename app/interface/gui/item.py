from tkinter import *


class Item(Frame):
    def __init__(self, master, time: str, message: str, cnf=None, **kw):
        if cnf is None:
            cnf = {}
        super().__init__(master, cnf, **kw)

        Label(self, text=time).grid(row=0, column=0)
        Label(self, text=message).grid(row=0, column=5)
