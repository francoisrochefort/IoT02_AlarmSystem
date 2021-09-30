from tkinter import *
from tkinter import ttk
from eventlog import EventLog


# history window
class HistoryWindow(Frame):

    # event handlers
    def on_destroy_window(self):
        self.master.destroy()

    # class constructor
    def __init__(self, master=None):

        # init. window
        super().__init__(master)
        self.master = master
        self.master.title("History")
        self.master.geometry("400x225")
        self.master.protocol("WM_DELETE_WINDOW", lambda: self.on_destroy_window())
        self.pack(anchor=W)

        # columns
        columns = ('#1', '#2', '#3', '#4')

        tree = ttk.Treeview(self, columns=columns, show='headings')

        # headings
        tree.heading('#1', text='Date')
        tree.heading('#2', text='Time')
        tree.heading('#3', text='Object')
        tree.heading('#4', text='Event')

        # event logs
        event_log: EventLog = EventLog()
        for event in event_log.get_event_logs():
            tree.insert('', END, values=f"{event['date']} {event['time']} {event['object']} {event['event']}")
        tree.pack(anchor=W)

        # free unused object
        del event_log
