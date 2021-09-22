import struct
import pyaudio
import pvporcupine


class Hotword:
    def __init__(self):
        self.keywords=["picovoice", "blueberry"]
        self.porcupine = pvporcupine.create(keywords=self.keywords)
        
    def __del__(self):
        self.porcupine.delete()
        
    def wait(self):
        try:
            pa = pyaudio.PyAudio()
            audio_stream = pa.open(
                            rate=self.porcupine.sample_rate,
                            channels=1,
                            format=pyaudio.paInt16,
                            input=True,
                            frames_per_buffer=self.porcupine.frame_length)

            while True:
                pcm = audio_stream.read(self.porcupine.frame_length)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                keyword_index = self.porcupine.process(pcm)
                if keyword_index >= 0:
                    break
        finally:
            if audio_stream is not None:
                audio_stream.close()
            if pa is not None:
                pa.terminate()

        
if __name__ == "__main__":
    hotword = Hotword()
    print(hotword.keywords)
    hotword.wait()
    print("Le 'hotword' est detecte")
    

