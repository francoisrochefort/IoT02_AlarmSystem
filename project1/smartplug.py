from RPiSim import GPIO
import time
import sys
import signal
from ismartplug import ISmartPlug
from ismartpluglistener import ISmartPlugListener
from eventlog import EventLog


# event logging
OBJECT_NAME = 'smartplug'
EVENT_ON = 'on'
EVENT_OFF = 'off'


# gpio pin assignments
BOUTON_PIN  = 17
LUMIERE_PIN = 18
DEL_PIN     = 23


class SmartPlug(ISmartPlug):

    # smartplug interface implementation
    def turn_on(self):

        # turn on the light
        GPIO.output(LUMIERE_PIN, GPIO.HIGH)
        if self.listener is not None:
            self.listener.on_smartplug_on()
            self.event_log.write_event(OBJECT_NAME, EVENT_ON)

    def turn_off(self):

        # turn off the light
        GPIO.output(LUMIERE_PIN, GPIO.LOW)
        if self.listener is not None:
            self.listener.on_smartplug_off()
            self.event_log.write_event(OBJECT_NAME, EVENT_OFF)

    # call by the system
    def terminate(self, signum, frame):
        GPIO.output(LUMIERE_PIN, GPIO.LOW)
        GPIO.cleanup()
        sys.exit(0)

    # gpio callback functions
    def event_bouton(self, channel):

        if GPIO.input(LUMIERE_PIN):
            self.turn_off()
        else:
            self.turn_on()

    def __init__(self, listener: ISmartPlugListener = None):

        # init. class attributes
        self.listener: ISmartPlugListener = listener
        self.event_log: EventLog = EventLog()

        signal.signal(signal.SIGINT, lambda signum, frame: self.terminate(signum, frame))

        # inti. gpio
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # on/off button
        GPIO.setup(BOUTON_PIN,GPIO.MODE_IN,pull_up_down = GPIO.PUD_UP) 
        GPIO.add_event_detect(BOUTON_PIN, GPIO.FALLING, callback=lambda channel: self.event_bouton(channel))

        # light itself
        GPIO.setup(LUMIERE_PIN,GPIO.MODE_OUT, initial=GPIO.LOW)

        
if __name__ == "__main__":
    smartplug: SmartPlug = SmartPlug()
    while True:
        time.sleep(0.5)
