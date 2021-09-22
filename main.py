from hotword import Hotword
from speech import Speech
from fuzzywuzzy import process


def main():

    while True:

        # wait for the user to say the hot word
        hotword: Hotword = Hotword()
        hotword.wait()

        # tell the user the program is awaiting a command
        Speech.say("Comment puis-je vous aider?")

        # capture the user's command
        command = u"quel temps il fait?"

        # guess what command the user just said
        commands = [u"quelle heure est-il?", 
                    u"il est quelle heure?", 
                    u"quel temps fait-il?", 
                    u"quelles sont les prévision météo?", 
                    u"quelles sont les prévisions de la météo?"]
        (modele, score) = process.extractOne(command, commands)
        print(modele, score)


if __name__ == "__main__":
    main()