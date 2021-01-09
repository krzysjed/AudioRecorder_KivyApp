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
import pickle
import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
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

    def send(self):
        Upload()




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


class Upload:
    def __init__(self):
        self.CLIENT_SECRET_FILE = 'wavereco_test_pc.json'  # ! remember to change !
        self.API_NAME = 'drive'
        self.API_VERSION = 'v3'
        self.SCOPES = ['https://www.googleapis.com/auth/drive']  # full scope

    # creating service
        self.service = self.authorization(self.CLIENT_SECRET_FILE, self.API_NAME, self.API_VERSION, self.SCOPES)

    # uploading file
    # if user_email and access = None uploaded file won't be shared
        self.upload(folder_name="test_folder", file_name="output.wav",
           user_email="mikolaj.telec@gmail.com", access="reader",
           file_mime="audio / wav")

    def authorization(self,client_secret_file, api_name, api_version, scope):

        creds = None

        # loads already created token
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # no previously created token or token is expired
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())  # token refreshing
            else:
                flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scope)  # token generation
                creds = flow.run_local_server(port=0)
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)  # saving access token in token.pickle

        # creating Resource for interaction with API
        drive_service = build(api_name, api_version, credentials=creds, )

        return drive_service

    def upload(self,folder_name, file_name, user_email=None, access=None, file_mime='audio / wav'):

        # creating folder
        mime = 'application/vnd.google-apps.folder'  # MIME type - identifies file format
        folder_metadata = {  # resources are represented by metadata
            'name': folder_name,
            'mimeType': mime
        }
        folder = self.service.files().create(body=folder_metadata, fields='id').execute()  # creates folder
        folder_identifier = folder.get('id')  # gets folder id for creating permission

        # adding permission to folder and it's content if...
        if user_email and access:
            permission_body = {
                "kind": "drive#permission",
                "type": "user",
                "emailAddress": user_email,
                "role": access
            }
            self.service.permissions().create(fileId=folder_identifier, body=permission_body).execute()

        # uploading file
        file_metadata = {  # resources are represented by metadata
            'name': file_name,
            'parents': [folder_identifier]  # ID of parent folder
        }

        # creating MediaFileUpload object
        media = MediaFileUpload(file_name, mimetype=file_mime)
        self.service.files().create(  # creates file based on file and media metadata
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        return None


MyPaintApp().run()
