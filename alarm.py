from enum import Enum
from RPiSim import GPIO
from threading import Thread
import sys
import signal
import time
from ialarmlistener import IAlarmListener
from ialarm import IAlarm
from eventlog import EventLog


# event logging
OBJECT_NAME = 'alarm'
EVENT_ON = 'on'
EVENT_OFF = 'off'
EVENT_ALARM = 'alarm!'


# gpio pin assignments
DOOR_PIN = 5
BUTTON_PIN = 17
BUZZER_PIN = 18
DEL_PIN = 23


# alarm states
class State(Enum):
    OFF = 1
    DELAY_E = 2
    ARMED = 3
    DELAY_S = 4
    BUZZER = 5


# input events
class Event(Enum):
    DOOR = 1
    ARM = 2
    CODE = 3
    BUTTON_INTERFACE = 4
    END_DELAY = 5


class Alarm(IAlarm):

    # alarm interface implementation
    def turn_on(self):
        self.set_state(Event.BUTTON_INTERFACE, 'ON')

    def turn_off(self):
        self.set_state(Event.BUTTON_INTERFACE, 'OFF')

    # call by the system
    def terminate(self, signum, frame):
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        GPIO.cleanup()
        sys.exit(0)

    # gpio callback functions
    def event_arm(self, channel):
        self.set_state(Event.ARM)

    def event_door(self, channel):
        self.set_state(Event.DOOR)

    # class constructor
    def __init__(self, listener: IAlarmListener = None) -> None:

        # init. class attributes
        self.State = State.OFF
        self.listener: IAlarmListener = listener
        self.event_log: EventLog = EventLog()

        signal.signal(signal.SIGINT, lambda signum, frame: self.terminate(signum, frame))

        # init. gpio
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # button pin setup
        GPIO.setup(BUTTON_PIN, GPIO.MODE_IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=lambda channel: self.event_arm(channel))

        # door pin setup
        GPIO.setup(DOOR_PIN, GPIO.MODE_IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(DOOR_PIN, GPIO.FALLING, callback=lambda channel: self.event_door(channel))

        # buzzer pin setup
        GPIO.setup(BUZZER_PIN, GPIO.MODE_OUT, initial=GPIO.LOW)

        # led pin setup
        GPIO.setup(DEL_PIN, GPIO.MODE_OUT, initial=GPIO.LOW)

    def set_state(self, event, command=''):

        if event == Event.ARM:
            if self.State == State.OFF:
                self.State = State.DELAY_S
                thread = Thread(target=lambda: self.blink_led(), args=())
                thread.start()

            elif self.State == State.ARMED:
                self.State = State.OFF
                GPIO.output(DEL_PIN, GPIO.LOW)
                GPIO.output(BUZZER_PIN, GPIO.LOW)
                self.event_log.write_event(OBJECT_NAME, EVENT_OFF)
                if self.listener is not None:
                    self.listener.on_alarm_off()
                
            elif self.State == State.DELAY_S:
                self.State = State.OFF
                GPIO.output(DEL_PIN, GPIO.LOW)
                self.event_log.write_event(OBJECT_NAME, EVENT_OFF)
                if self.listener is not None:
                    self.listener.on_alarm_off()

            elif self.State == State.BUZZER:
                self.State = State.OFF
                GPIO.output(DEL_PIN, GPIO.LOW)
                GPIO.output(BUZZER_PIN, GPIO.LOW)
                self.event_log.write_event(OBJECT_NAME, EVENT_OFF)
                if self.listener is not None:
                    self.listener.on_alarm_off()
    
            elif self.State == State.DELAY_E:
                self.State = State.OFF
                GPIO.output(DEL_PIN, GPIO.LOW)
                self.event_log.write_event(OBJECT_NAME, EVENT_OFF)
                if self.listener is not None:
                    self.listener.on_alarm_off()

        elif event == Event.END_DELAY:
            if self.State == State.DELAY_S:
                self.State = State.ARMED
                GPIO.output(DEL_PIN, GPIO.HIGH)
                self.event_log.write_event(OBJECT_NAME, EVENT_ON)
                if self.listener is not None:
                    self.listener.on_alarm_on()
                
            elif self.State == State.DELAY_E:
                self.State = State.BUZZER
                GPIO.output(BUZZER_PIN, GPIO.HIGH)
                self.event_log.write_event(OBJECT_NAME, EVENT_ALARM)
                if self.listener is not None:
                    self.listener.on_alarm_ring()
                
        elif event == Event.DOOR:
            if self.State == State.ARMED:
                self.State = State.DELAY_E
                thread = Thread(target=lambda: self.blink_led(), args=())
                thread.start()

        if event == Event.BUTTON_INTERFACE:
            if command == 'ON':
                self.State = State.ARMED
                GPIO.output(DEL_PIN, GPIO.HIGH)
                self.event_log.write_event(OBJECT_NAME, EVENT_ON)
                if self.listener is not None:
                    self.listener.on_alarm_on()

            else:
                self.State = State.OFF
                GPIO.output(DEL_PIN, GPIO.LOW)
                GPIO.output(BUZZER_PIN, GPIO.LOW)
                self.event_log.write_event(OBJECT_NAME, EVENT_OFF)
                if self.listener is not None:
                    self.listener.on_alarm_off()

    def blink_led(self):
        DELAY = 5
        delay = 0
        while delay <= DELAY:
            if self.State == State.OFF:
                return
            if GPIO.input(DEL_PIN):
                GPIO.output(DEL_PIN, GPIO.LOW)
            else:
                GPIO.output(DEL_PIN, GPIO.HIGH)
            time.sleep(1)
            delay += 1
        self.set_state(Event.END_DELAY)


if __name__ == "__main__":
    alarm: Alarm = Alarm()
    while True:
        time.sleep(0.5)
