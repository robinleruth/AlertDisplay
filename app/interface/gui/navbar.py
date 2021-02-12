from tkinter import *


class Navbar(Frame):
    def __init__(self, master, cnf=None, **kw):
        if cnf is None:
            cnf = {}
        super().__init__(master, cnf, **kw)
        self.parent = master
        self.lookup_table = {
            '1': 'Alerts',
            '2': 'CronTab',
            '3': 'Cron rules'
        }

        Label(self, text='Navbar').pack()
        self.var = IntVar(value=1)
        Radiobutton(self, text='Alerts', variable=self.var, value=1, command=self.sel).pack()
        Radiobutton(self, text='CronTab', variable=self.var, value=2, command=self.sel).pack()
        Radiobutton(self, text='Cron rules', variable=self.var, value=3, command=self.sel).pack()

    def sel(self):
        self.parent.switch_main(self.lookup_table[str(self.var.get())])
