import speech_recognition as sr
import asyncio
import time


class SpeechToText:
    def __init__(self):
        self.r = sr.Recognizer()
        self.r.energy_threshold = 50
        self.r.pause_threshold = 0.5
        self.results = []

    async def process(self):
        with sr.Microphone() as source:
            while True:
                audio = self.r.listen(source, phrase_time_limit=3, timeout=10)

                try:
                    text = self.r.recognize_google(audio)
                    self.results.append(text)
                except sr.UnknownValueError:
                    print("Sorry could not recognize what you said!")
                except sr.RequestError as e:
                    print(
                        "Could not request results from Google Speech Recognition service; {0}".format(
                            e
                        )
                    )

    def start(self):
        asyncio.get_event_loop().run_until_complete(self.process())

    def get(self):
        if len(self.results) == 0:
            return 0

        return self.results.pop(0)


stt = SpeechToText()
stt.start()
time.sleep(10)
