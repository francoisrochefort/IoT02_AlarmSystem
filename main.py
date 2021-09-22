from re import match
from hotword import Hotword
from speech import Speech
from fuzzywuzzy import process
from project1.ialarm import IAlarm
from project1.alarmproxy import AlarmProxy


# text commands
CMD_TURN_ON_ALARM = u"Armer le systeme d'alarme"
CMD_TURN_OFF_ALARM = u"Desarmer le systeme d'alarme"


# main program
def main():

    # create an alarm object
    alarm: IAlarm = AlarmProxy()

    while True:

        # wait for the user to say the hot word
        hotword: Hotword = Hotword()
        hotword.wait()

        # tell the user the program is awaiting a command
        Speech.say("Comment puis-je vous aider?")

        # capture the user's command (July, c'est ici qu'il faut ajouter le code avec wit.ai)
        command = CMD_TURN_ON_ALARM

        # guess what command the user just said
        commands = [CMD_TURN_ON_ALARM,
                    CMD_TURN_OFF_ALARM]
        (match, score) = process.extractOne(command, commands)

        # execute the command
        if match == CMD_TURN_ON_ALARM:
            alarm.turn_on()


# program entry point
if __name__ == "__main__":
    main()