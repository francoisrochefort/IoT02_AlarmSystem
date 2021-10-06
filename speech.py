from gtts import gTTS
import subprocess


class Speech:

    def __init__(self):
        pass

    @staticmethod
    def say(text: str):

        tts = gTTS(text, lang="en")
        tts.save('out.mp3')
        cmd = ['mpg321', '-q', 'out.mp3']
        subprocess.call(cmd)


if __name__ == '__main__':
    Speech.say("belles boules")
