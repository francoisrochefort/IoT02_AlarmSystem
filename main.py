from re import match
from hotword import Hotword
from speech import Speech
from fuzzywuzzy import process
from project1.ialarm import IAlarm
from project1.alarmproxy import AlarmProxy
from project1.ismartplug import ISmartPlug
from project1.smartplug import SmartPlugStub


# text commands
CMD_TURN_ON_ALARM = u"Armer le systeme d'alarme"
CMD_TURN_OFF_ALARM = u"Desarmer le systeme d'alarme"
CMD_TURN_ON_SMARTPLUG = u"Allumer la lumiere"
CMD_TURN_OFF_SMARTPLUG = u"Fermer la lumiere"


# main program
def main():

    # create an alarm object
    alarm: IAlarm = AlarmProxy()
    smartplug: ISmartPlug = SmartPlugStub()

    while True:

        # wait for the user to say the hot word
        hotword: Hotword = Hotword()
        hotword.wait()

        # tell the user the program is awaiting a command
        Speech.say("Comment puis-je vous aider?")

        # TODO: capture the user's command (July's task)
        command = CMD_TURN_ON_ALARM

        # guess what command the user just said
        commands = [CMD_TURN_ON_ALARM,
                    CMD_TURN_OFF_ALARM,
                    CMD_TURN_ON_SMARTPLUG,
                    CMD_TURN_OFF_SMARTPLUG]
        (match, score) = process.extractOne(command, commands)

        # execute the command
        if match == CMD_TURN_ON_ALARM:
            alarm.turn_on()
        elif match == CMD_TURN_OFF_ALARM:
            alarm.turn_off()
        elif match == CMD_TURN_ON_SMARTPLUG:
            smartplug.turn_on()
        elif match == CMD_TURN_OFF_SMARTPLUG:
            smartplug.turn_on()


# program entry point
if __name__ == "__main__":
    main()