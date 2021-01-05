from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from functools import partial
import sounddevice as sd
from scipy.io.wavfile import write
from scipy.io import wavfile
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import os
kv = Builder.load_file("style.kv")

class MainWindow(Screen):
    def play(self):
        try:
            fs = 44000
            sample, data = wavfile.read('output.wav')
            sd.play(data, fs)
            sd.wait()
        except IOError:
            self.play_btn.text = "No file!"

    def record(self):

        if self.rec_btn.text == "Record":
            self.rec_btn.text = "Recorded"
            fs = 44000  # sampling
            seconds = 5  # duration of recording
            myrecording = sd.rec(seconds * fs, samplerate=fs, channels=2)
            sd.wait()  # Wait until recording is finished
            write('output.wav', fs, myrecording)
            self.del_Btn.color = 1, 1, 1, 0.7
            self.del_Btn.background_color = 0, 0, 0, .5

    def delete(self):
        try:
            os.remove('output.wav')
            self.rec_btn.text = "Record"
        except IOError:
            pass
        self.del_Btn.color = 1, 1, 1, 0.2
        self.del_Btn.background_color = 0, 0, 0, 0.2


class AfterRecordWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


sm = ScreenManager()
sm.add_widget(MainWindow(name="main"))
sm.add_widget(AfterRecordWindow(name="second"))


class MyPaintApp(App):

    def build(self):
        return sm

MyPaintApp().run()
