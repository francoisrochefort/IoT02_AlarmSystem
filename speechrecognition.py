from threading import Thread
import threading
from hotword import Hotword
from speech import Speech
from fuzzywuzzy import process
from ialarm import IAlarm
from alarmproxy import AlarmProxy
from ismartplug import ISmartPlug
from smartplugproxy import SmartPlugProxy


# text commands
CMD_TURN_ON_ALARM = u"Armer le systeme d'alarme"
CMD_TURN_OFF_ALARM = u"Desarmer le systeme d'alarme"
CMD_TURN_ON_SMARTPLUG = u"Allumer la lumiere"
CMD_TURN_OFF_SMARTPLUG = u"Fermer la lumiere"


class SpeechRecognition(threading.Thread):

    def __init__(self, alarm: IAlarm, smartplug: ISmartPlug) -> None:

        # init. the thread
        threading.Thread.__init__(self)

        # init. speech recognition attributes
        self.alarm: IAlarm = alarm
        self.smartplug: ISmartPlug = smartplug

    def run(self) -> None:

        while True:

            # wait for the user to say any hot word
            hotword: Hotword = Hotword()
            hotword.wait()

            # tell the user the program is awaiting a command
            Speech.say("Comment puis-je vous aider?")

            # TODO: capture the user's voice command
            command = CMD_TURN_ON_ALARM

            # guess what command the user just said
            commands = [CMD_TURN_ON_ALARM,
                        CMD_TURN_OFF_ALARM,
                        CMD_TURN_ON_SMARTPLUG,
                        CMD_TURN_OFF_SMARTPLUG]
            (match, score) = process.extractOne(command, commands)

            # execute the command
            if match == CMD_TURN_ON_ALARM:
                self.alarm.turn_on()
            elif match == CMD_TURN_OFF_ALARM:
                self.alarm.turn_off()
            elif match == CMD_TURN_ON_SMARTPLUG:
                self.smartplug.turn_on()
            elif match == CMD_TURN_OFF_SMARTPLUG:
                self.smartplug.turn_on()


# program entry point
if __name__ == "__main__":

    task: SpeechRecognition = SpeechRecognition(AlarmProxy(), SmartPlugProxy())
    task.start()
