
from kivy.core.window import Window
from kivy.app import App
import sounddevice as sd
from scipy.io.wavfile import write
from scipy.io import wavfile
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import os
from kivy.uix.switch import  Switch
from kivy.uix.settings import SettingsWithTabbedPanel
from settingsjson import settings_json
from kivy.config import Config

Builder.load_file("style.kv")


class MainWindow(Screen):
    def __init__(self, config_data):
        super(MainWindow, self).__init__()
        self.config_data = config_data

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
            fs = 44000  # sampling max  384000  ;p
            seconds = 10  # duration of recording
            myrecording = sd.rec(seconds * fs, samplerate=fs, channels=int(self.config_data.get('example', 'channelsetting')))
            print(self.config_data.get('example', 'channelsetting'))
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

    def exit(self):
        App.get_running_app().stop()
        Window.close()


class AfterRecordWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class SettingsScreen(Screen):
    pass


class MyPaintApp(App):

    def build(self):

        self.settings_cls = SettingsWithTabbedPanel
        self.use_kivy_settings = False

        sm = ScreenManager()

        #sm.add_widget(SettingsScreen(name='settings'))
        #settings = self.config.get('example', 'channelsetting')

        sm.add_widget(MainWindow(self.config))
        return sm

    def build_config(self, config):
        config.setdefaults('example', {
            'ChannelSetting': '2',
            'ExtensionSetting':'.wav',
            'stringexample': 'some_string',
            'pathexample': '/some/path'})

    def build_settings(self, settings):

        settings.add_json_panel('Audio',
                                self.config,
                                data=settings_json)

        settings.add_json_panel('Cloud',
                                self.config,
                                data=settings_json)

        settings.add_json_panel('Another itd',
                                self.config,
                                data=settings_json)

    def on_config_change(self, config, section, key, value):
        print(config, section, key, value)


MyPaintApp().run()
