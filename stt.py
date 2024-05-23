import speech_recognition as sr
from threading import Lock


class SpeechToText:
    def __init__(self):
        self.r = sr.Recognizer()
        self.r.energy_threshold = 50
        self.r.pause_threshold = 0.5
        self.results = []
        self.lock: Lock = Lock()

    def process(self):
        with sr.Microphone() as source:
            while True:
                audio = self.r.listen(source, phrase_time_limit=3, timeout=10)

                try:
                    text = self.r.recognize_google(audio)
                    self.lock.acquire()
                    self.results.append(text)
                    self.lock.release()
                except sr.UnknownValueError:
                    print("Sorry could not recognize what you said!")
                except sr.RequestError as e:
                    print(
                        "Could not request results from Google Speech Recognition service; {0}".format(
                            e
                        )
                    )

    def get(self):
        ret = None
        self.lock.acquire()
        if len(self.results) != 0:
            ret = self.results.pop(0)
        self.lock.release()
        return ret
