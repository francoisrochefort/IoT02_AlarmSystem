from enum import Enum
from tkinter import *
from historywindow import HistoryWindow
from ialarmlistener import IAlarmListener
from ialarm import IAlarm
from alarmproxy import AlarmProxy
from ismartpluglistener import ISmartPlugListener
from ismartplug import ISmartPlug
from smartplugproxy import SmartPlugProxy
from speechrecognition import SpeechRecognition


# IntVar possible values
OFF = 0
ON = 1


# main window
class MainWindow(Frame, IAlarmListener, ISmartPlugListener):

    # widget command handlers
    def on_turn_alarm_on(self):
        self.alarm.turn_on()

    def on_turn_alarm_off(self):
        self.alarm.turn_off()

    def on_turn_smartplug_on(self):
        self.smartplug.turn_on()

    def on_turn_smartplug_off(self):
        self.smartplug.turn_off()

    def on_show_history(self):
        window = HistoryWindow(master=Tk())

    def on_destroy_window(self):
        del self.alarm
        del self.smartplug
        self.master.destroy()

    # class constructor
    def __init__(self, master):

        # init. the window
        super().__init__(master, padx=10, pady=10)
        self.master.title("IoT Remote Controller")
        self.master.protocol("WM_DELETE_WINDOW", lambda: self.on_destroy_window())
        self.pack(anchor=W)

        # init. a widget bound variables
        self.alarm_state: IntVar = IntVar()
        self.smartplug_state: IntVar = IntVar()

        # create alarm widgets
        frame = Frame(self, relief=GROOVE, bd=2, padx=10, pady=10)
        frame.pack(anchor=W)
        Label(frame, text="Alarm:").pack(anchor=W)
        Radiobutton(frame,
                    text="OFF",
                    variable=self.alarm_state,
                    value=OFF,
                    command=self.on_turn_alarm_off).pack(anchor=W)
        Radiobutton(frame,
                    text="ON",
                    variable=self.alarm_state,
                    value=ON,
                    command=self.on_turn_alarm_on).pack(anchor=W)

        # create smartplug widgets
        frame = Frame(self, relief=GROOVE, bd=2, padx=10, pady=10)
        frame.pack(anchor=W)
        Label(frame, text="Smartplug:").pack(anchor=W)
        Radiobutton(frame,
                    text="OFF",
                    variable=self.smartplug_state,
                    value=OFF,
                    command=self.on_turn_smartplug_off).pack(anchor=W)
        Radiobutton(frame,
                    text="ON",
                    variable=self.smartplug_state,
                    value=ON,
                    command=self.on_turn_smartplug_on).pack(anchor=W)

        # create history widgets
        frame = Frame(self, relief=GROOVE, bd=2, padx=10, pady=10)
        frame.pack(anchor=W)
        Label(frame, text="History:").pack(anchor=W)
        Button(frame, text="History...", command=self.on_show_history).pack(anchor=W)

        # create both remote objects
        self.alarm: IAlarm = AlarmProxy(self)
        self.smartplug: ISmartPlug = SmartPlugProxy(self)
        self.speech_recognition = SpeechRecognition(self.alarm, self.smartplug)
        self.speech_recognition.start()

    # alarm listener interface implementation
    def on_alarm_on(self):
        self.alarm_state.set(ON)
 
    def on_alarm_off(self):
        self.alarm_state.set(OFF)
 
    def on_alarm_ring(self):
        self.master.title("CALL 911 - ALARM!")

    # smartplug listener interface implementation
    def on_smartplug_on(self):
        self.smartplug_state.set(ON)
 
    def on_smartplug_off(self):
        self.smartplug_state.set(OFF)

