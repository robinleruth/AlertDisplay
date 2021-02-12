from tkinter import *


class Input(Frame):
    def __init__(self, master, cnf=None, **kw):
        if cnf is None:
            cnf = {}
        super().__init__(master, cnf, **kw)

        Label(self, text="time").grid(row=0, column=0)
        Label(self, text="message").grid(row=0, column=5)
        self.e1 = Entry(self)
        self.e2 = Entry(self)
        self.e1.grid(row=3, column=0)
        self.e2.grid(row=3, column=5)

        Button(self, text="Schedule !", command=self.schedule).grid(row=5, column=3)  # ,  sticky=W, pady=4)

    def schedule(self):
        self.master.master.master.out_queue.put((self.e1.get(), self.e2.get()))

    def clear(self):
        self.e1.delete(0, 'end')
        self.e2.delete(0, 'end')
