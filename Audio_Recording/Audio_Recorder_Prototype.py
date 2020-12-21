from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
import sounddevice as sd
from scipy.io.wavfile import write
from scipy.io import wavfile


def play(*arg ):  # play recording from file wav audio 
    fs = 44000
    sample, data=wavfile.read('output.wav')
    sd.play(data, fs)
    sd.wait()


def record(*arg): # record & save audio to output.wav

    fs = 44000  # sampling
    seconds = 5  # duration of recording

    myrecording = sd.rec(seconds * fs, samplerate=fs, channels=2)

    sd.wait()  
    write('output.wav', fs, myrecording)

    print("End_Recording")

class MyPaintApp(App):
    def build(self):
        y=Button(size_hint=(0.2,0.2), pos=(200,200), text="Record", on_press=record)
        x=Button(size_hint=(0.2,0.2), pos=(400,400), text="Play", on_press=play)
        r1=RelativeLayout(size=(300,300))
        r1.add_widget(y)
        r1.add_widget(x)
        return r1


MyPaintApp().run()
