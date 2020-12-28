from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from functools import partial
import sounddevice as sd
from scipy.io.wavfile import write
from scipy.io import wavfile
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
kv = Builder.load_file("style.kv")


class MainWindow(Screen):
    def play(self):
        fs = 44000
        sample, data = wavfile.read('output.wav')
        sd.play(data, fs)
        sd.wait()
        print("end play")

    def record(self):
        if self.rec_btn.text == "Record":
            self.rec_btn.text = "Stop"
        fs = 44000  # sampling
        seconds = 5  # duration of recording
        myrecording = sd.rec(seconds * fs, samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        write('output.wav', fs, myrecording)

        print("END")

    pass


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
