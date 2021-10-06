from threading import Thread
import threading
from hotword import Hotword
from speech import Speech
from fuzzywuzzy import process
from ialarm import IAlarm
from alarmproxy import AlarmProxy
from ismartplug import ISmartPlug
from smartplugproxy import SmartPlugProxy
from datetime import date, datetime
from STT_convert import STT_phrase



# text commands
CMD_TURN_ON_ALARM = u"Alarm_on"
CMD_TURN_OFF_ALARM = u"Alarm_off"
CMD_TURN_ON_SMARTPLUG = u"Lights_on"
CMD_TURN_OFF_SMARTPLUG = u"Lights_off"
CMD_WHAT_TIME = u"Actual_Time"
CMD_WHAT_DATE = u"Actual_day"
NO_COMMAND = u"Nothing"
UNKNOWN_COMMAND = u"Unknown"


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
            Speech.say("How can I help you?")

            """Enregistrer ave pyaudio un stream et l'envoyer à
            wit.ai pour recoir l''intent qui sera la commande a executer"""


            phrase = STT_phrase()
            match= phrase.wait()

            # execute the command
            if match == CMD_TURN_ON_ALARM:
                self.alarm.turn_on()
            elif match == CMD_TURN_OFF_ALARM:
                self.alarm.turn_off()
            elif match == CMD_TURN_ON_SMARTPLUG:
                self.smartplug.turn_on()
            elif match == CMD_TURN_OFF_SMARTPLUG:
                self.smartplug.turn_off()
            elif match == CMD_WHAT_TIME:
                now = datetime.now()
                current_time = now.strftime("%H:%M")
                text2say = "The time is" + str(current_time)
                Speech.say(text2say)
            elif match == CMD_WHAT_DATE:
                today = date.today()
                current_date = today.strftime("%d %B, %Y")
                print("d2 =", current_date)
                text2say = "We are" + str(current_date)
                Speech.say(text2say)
            elif match == NO_COMMAND:
                text2say = "I heard nothing"
                Speech.say(text2say)
            elif match == UNKNOWN_COMMAND:
                text2say = "I do not understand"
                Speech.say(text2say)










# program entry point
if __name__ == "__main__":

    task: SpeechRecognition = SpeechRecognition(AlarmProxy(), SmartPlugProxy())
    task.start()
