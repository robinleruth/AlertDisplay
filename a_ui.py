from tkinter import *
from tkinter.ttk import *

import matplotlib
import pandas as pd

matplotlib.use('TkAgg')
from matplotlib import pyplot as plt, animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

style.use('ggplot')

TITLE_FONT = ("Helvetica", 11)
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

f = plt.figure()
a = f.add_subplot(111)

darkColor = '#183A54'
lightColor = '#00A3E0'


def popup_msg(msg):
    popup = Tk()

    def leave_mini():
        popup.destroy()

    popup.wm_title("!")

    label = Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    b = Button(popup, text="Okay", command=leave_mini)
    b.pack()

    popup.mainloop()


def pop_new_window(window):
    window().mainloop()


class MyApp(Tk):
    def __init__(self, *args, **kwargs):

        Tk.__init__(self, *args, **kwargs)

        # menubar = Menu(Tk)

        style = Style()
        style.layout("Button", [
            ("Menubutton.background", None),
            ("Menubutton.foreground", None),
            ("Menubutton.button", {"children": [("Menubutton.focus", {"children": [
                ("Menubutton.padding", {"children": [("Menubutton.label", {"side": "left", "expand": 1})]})]})]}), ])

        style.layout("TMenubutton", [
            ("Menubutton.background", None),
            ("Menubutton.button", {"children": [("Menubutton.focus", {"children": [
                ("Menubutton.padding", {"children": [("Menubutton.label", {"side": "left", "expand": 1})]})]})]}), ])

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self, width=1280, height=720)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = Menu(container)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command=lambda: popup_msg('Not supported just yet!'))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Tutorial", command=lambda: popup_msg('Tutorial'))
        menubar.add_cascade(label="Help", menu=helpmenu)

        other_pages = Menu(menubar, tearoff=0)
        other_pages.add_command(label="Second page", command=lambda: self.show_frame(SecondPage))
        other_pages.add_command(label="Dashboard", command=lambda: self.show_frame(MyNotebook))
        other_pages.add_command(label="Grid", command=lambda: self.show_frame(MyNotebook))
        menubar.add_cascade(label="JUMP", menu=other_pages)

        new_window = Menu(menubar, tearoff=0)
        new_window.add_command(label="Open in new window", command=lambda: pop_new_window(MyApp))
        menubar.add_cascade(label="New window", menu=new_window)

        Tk.config(self, menu=menubar)
        # editmenu.add_separator()
        # menubar.add_cascade(label="Edit", menu=filemenu)
        # container.title('test')

        self.frames = {}
        for F in (StartPage, Dashboard, SecondPage, MyNotebook):
            frame = F(container, self)
            self.frames[F] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(SecondPage)

        try:
            Tk.wm_title(self, "My application")
            Tk.iconbitmap(self, default='clienticon.ico')
        except Exception as e:
            print(str(e))

    def show_frame(self, c):
        '''Show a frame for the given class'''
        frame = self.frames[c]
        frame.tkraise()


class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="""
        Welcome
        """, font=TITLE_FONT)

        label.pack(side="top", fill="x", pady=10)

        button1 = Button(self, text="Go", command=lambda: controller.show_frame(Dashboard))
        button1.pack()


class SecondPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="""
        Second PAGE !!
        """, font=TITLE_FONT)

        label.pack(side="top", fill="x", pady=10)

        # Button(self, text="Go to dashboard", command=lambda: controller.show_frame(Dashboard)).pack()
        Button(self, text="Go to main frame", command=lambda: controller.show_frame(MyNotebook)).pack()
        self.v = StringVar()
        Label(self, textvariable=self.v).pack()
        Entry(self, textvariable=self.v).pack()


class MyNotebook(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Main frame", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)

        notebook = Notebook(self)
        notebook.add(Dashboard(notebook, controller), text="Dashboard")
        notebook.add(MyGrid(notebook), text="Grid")
        notebook.add(Frame(notebook), text="test3")
        notebook.pack()


lst = [
    [3, 2],
    [5, 2],
    [1, 3]
]

vars = {}


class MyGrid(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.vars = {}

        def callback(s, *args):
            print(s, *args)
            point = s.split(':')
            x = int(point[0])
            y = int(point[1])
            try:
                lst[x][y] = float(self.vars[s].get())
                for var in vars[s]:
                    var.value = self.vars[s].get()
            except Exception as e:
                print(e)

        for i in range(len(lst)):
            for j in range(len(lst[0])):
                name = f'{i}:{j}'
                v = StringVar(self, value=lst[i][j], name=name)
                v.callback = callback
                v.trace('w', v.callback)
                e = Entry(self, textvariable=v)
                e.grid(row=i, column=j)
                if name not in vars:
                    vars[name] = []
                vars[name].append(v)
                self.vars[name] = v
                # if (i, j) not in lst[i][len(lst)]:
                #     lst[i][len(lst)][(i, j)] = []
                # lst[i][len(lst)][(i, j)].append(v)  # maybe a weakref here is better ?


def load_chart(param):
    a.clear()
    df = pd.DataFrame(lst)
    a.plot(df[0], df[1])
    a.set_title('Title')


def change_exchange(param, param1):
    pass


def change_time_frame(param):
    pass


def change_sample_size(param, param1):
    pass


def add_top_indicator(param):
    pass


def add_middle_indicator(param):
    pass


def add_bottom_indicator(param):
    pass


class Dashboard(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # title and leading text #
        label = Label(self, text="Dashboard", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)

        # setting up the frame #
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=BOTTOM, fill=BOTH, expand=1)

        mb = Menubutton(self, text="Resume/Pause Updates")
        mb.menu = Menu(mb, tearoff=0)
        mb["menu"] = mb.menu
        mb.menu.add_command(label="Resume", command=lambda: load_chart('start'))
        mb.menu.add_command(label="Pause", command=lambda: load_chart('stop'))
        mb.pack(side='right')

        mb = Menubutton(self, text="Exchange")
        mb.menu = Menu(mb, tearoff=0)
        mb["menu"] = mb.menu
        mb.menu.add_command(label="BTC-e", command=lambda: change_exchange('BTC-e', 'btce'))
        mb.menu.add_command(label="Bitfinex", command=lambda: change_exchange('Bitfinex', 'bitfinex'))
        mb.menu.add_command(label="Bitstamp", command=lambda: change_exchange('Bitstamp', 'bitstamp'))
        mb.menu.add_command(label="Huobi", command=lambda: change_exchange('Huobi', 'huobi'))
        mb.pack(side='left')

        mb = Menubutton(self, text="Data Time Frame")
        mb.menu = Menu(mb, tearoff=0)
        mb["menu"] = mb.menu
        mb.menu.add_command(label="Tick", command=lambda: change_time_frame('tick'))
        mb.menu.add_command(label="1 day", command=lambda: change_time_frame('1d'))
        mb.menu.add_command(label="3 day", command=lambda: change_time_frame('3d'))
        mb.menu.add_command(label="1 Week", command=lambda: change_time_frame('7d'))
        mb.pack(side='left')

        mb = Menubutton(self, text="OHLC Interval")
        mb.menu = Menu(mb, tearoff=0)
        mb["menu"] = mb.menu
        mb.menu.add_command(label="Tick", command=lambda: change_time_frame('tick'))
        mb.menu.add_command(label="1 minute", command=lambda: change_sample_size('1Min', 0.0005))
        mb.menu.add_command(label="5 minute", command=lambda: change_sample_size('5Min', 0.003))
        mb.menu.add_command(label="15 minute", command=lambda: change_sample_size('15Min', 0.008))
        mb.menu.add_command(label="30 minute", command=lambda: change_sample_size('30Min', 0.016))
        mb.menu.add_command(label="1 Hour", command=lambda: change_sample_size('1H', 0.032))
        mb.menu.add_command(label="3 Hour", command=lambda: change_sample_size('3H', 0.096))

        mb.pack(side='left')

        mb = Menubutton(self, text="Top Indicator")
        mb.menu = Menu(mb, tearoff=0)
        mb["menu"] = mb.menu
        mb.menu.add_command(label="None", command=lambda: add_top_indicator('none'))
        mb.menu.add_command(label="RSI", command=lambda: add_top_indicator('rsi'))
        mb.menu.add_command(label="MACD", command=lambda: add_top_indicator('macd'))
        mb.pack(side='left')

        mb = Menubutton(self, text="Main Graph Indicator")
        mb.menu = Menu(mb, tearoff=0)
        mb["menu"] = mb.menu
        mb.menu.add_command(label="None", command=lambda: add_middle_indicator('none'))
        mb.menu.add_command(label="SMA", command=lambda: add_middle_indicator('sma'))
        mb.menu.add_command(label="EMA", command=lambda: add_middle_indicator('ema'))

        mb.pack(side='left')

        mb = Menubutton(self, text="Bottom Indicator")
        mb.menu = Menu(mb, tearoff=0)
        mb["menu"] = mb.menu
        mb.menu.add_command(label="None", command=lambda: add_bottom_indicator('none'))
        mb.menu.add_command(label="RSI", command=lambda: add_bottom_indicator('rsi'))
        mb.menu.add_command(label="MACD", command=lambda: add_bottom_indicator('macd'))
        mb.pack(side='left')


def animate(i):
    load_chart(i)


if __name__ == '__main__':
    app = MyApp()
    ani = animation.FuncAnimation(f, animate, interval=1000)
    app.mainloop()
