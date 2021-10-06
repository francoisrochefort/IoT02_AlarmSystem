# -*- coding: utf-8 -*-
'''
Created on 1 sept. 2021

@author: gills
'''
import json
import io
import requests
import pyaudio
import wave

# from speech_recognition import AudioData


class STT_phrase:
    def __init__(self):
        self.wit_api = 'https://api.wit.ai/speech'
        self.wit_key = "BBE6PH4CTNAAFAATWTXE465SRZCZ4PUP"
        self.wit_key_FR = 'NVRKGJKBJIN5OYURQSX453HGTWYILCKZ'
        self.listenTime = 4

    def wait(self):
        pa = pyaudio.PyAudio()

        #After that I am able to open the stream:
        RATE = 8000
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1

        '''
        Pour le déclanchement et la fin voir Speakerreconition.py
        La fonction Listen
        '''
        print('say something...')
        stream = pa.open(format=FORMAT, channels=CHANNELS,
                         rate=RATE, input=True, frames_per_buffer=CHUNK)

        frames = []

        for i in range(0, int(RATE / CHUNK * self.listenTime)):
            data = stream.read(CHUNK)
            frames.append(data)

        # stop Recording
        stream.stop_stream()
        stream.close()

        pa.terminate()

        audioOut = io.BytesIO()
        waveFile = wave.open(audioOut, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(pa.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        audioData = audioOut.getvalue()
        waveFile.close()

        HTTP_headers = {'Authorization': 'Bearer ' +
                       self.wit_key, 'Content-Type': 'audio/wav'}

        resp = requests.post(
            self.wit_api, headers=HTTP_headers, data= audioData)

        montest = resp.content.decode('utf-8')
        ma_reponse = montest.split( "\r")
        if len(ma_reponse) > 1 :
            last_index = (len(ma_reponse) -1)
            data = json.loads(ma_reponse[last_index])
            intent_wit = data['intents'][0]['name']
        else:
            intent_wit = "Nothing"
        return intent_wit

if __name__ == "__main__":
    phrase = STT_phrase()
    print("-> go")
    user_command = phrase.wait()
    print(" -> fin: " + user_command)
