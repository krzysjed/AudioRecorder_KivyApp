from kivy.core.window import Window
from kivy.app import App
import sounddevice as sd
from scipy.io.wavfile import write
from scipy.io import wavfile
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import os, shutil
import pathlib
from kivy.uix.popup import Popup
from kivy.uix.settings import SettingsWithTabbedPanel
from settingsjson import Recording_settings_json
from settingsjson import Upload_settings_json
import pickle
import os.path
import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from kivy.config import Config

from multiprocessing import Process, freeze_support

os.environ['KIVY_IMAGE'] = 'pil,sdl2'  # to add wallpaper (.exe)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Builder.load_file("style.kv")

try:
    os.mkdir("Audio_file")
    Common_path = pathlib.PurePath(pathlib.Path("Audio_file").parent.absolute(), pathlib.Path("Audio_file"))
except FileExistsError:
    Common_path = pathlib.PurePath(pathlib.Path("Audio_file").parent.absolute(), pathlib.Path("Audio_file"))


def external_play(cfg_get_sampling, selected_file):
    try:
        Window.close()
        fs = int(cfg_get_sampling)
        sample, data = wavfile.read(selected_file)
        sd.play(data, fs)
        sd.wait()
    except IOError:
        pass


def external_record(cfg_get_sampling, cfg_get_duration, cfg_get_channel, cfg_get_name, cfg_get_extension):
    Window.close()
    fs = int(cfg_get_sampling)
    seconds = int(cfg_get_duration)
    my_recording = sd.rec(seconds*fs, samplerate=fs, channels=int(cfg_get_channel))
    sd.wait()
    write(cfg_get_name+cfg_get_extension, fs, my_recording)

    while True:
        try:
            shutil.move(cfg_get_name + cfg_get_extension, Common_path)
            break
        except IOError:
            os.rename(cfg_get_name + cfg_get_extension, cfg_get_name + "0" + cfg_get_extension)
            cfg_get_name = cfg_get_name + "0"


class MainWindow(Screen):
    def __init__(self, config_data):
        super(MainWindow, self).__init__()
        self.config_data = config_data

    def play(self):
        self.play_btn.text = "Play!"
        try:
            playback_setting = self.config_data.get('Record', 'PlaybackSetting')
            selected_file = os.path.join(self.config_data.get('Record', 'PathSetting'))
            extension = os.path.splitext(selected_file)[-1].lower()
            if extension == ".mp3" or extension == ".flac" or extension == ".wav":
                sample, data = wavfile.read(selected_file)
                if playback_setting == '1':
                    fs = int(self.config_data.get('Record', 'SamplingSetting'))
                    sd.play(data, fs)
                else:

                    external_play_input_tuple = (self.config_data.get('Record', 'SamplingSetting'),
                                                 selected_file,)
                    p_play = Process(target=external_play, args=external_play_input_tuple)
                    p_play.start()

            else:
                self.play_btn.text = "Bad extension or luck file!"

        except IOError:
            self.play_btn.text = "No file!"

    def record(self):

        if self.rec_btn.text == "Record":
            self.rec_btn.text = "Recording"
            external_record_input_tuple = (self.config_data.get('Record', 'SamplingSetting'),
                                           self.config_data.get('Record', 'DurationSetting'),
                                           self.config_data.get('Record', 'ChannelSetting'),
                                           self.config_data.get('Record', 'File_Name'),
                                           self.config_data.get('Record', 'ExtensionSetting'))
            p_record = Process(target=external_record, args=external_record_input_tuple)
            p_record.start()

            self.rec_btn.text = "Record"
            # self.del_Btn.color = 1, 1, 1, 0.7
            # self.del_Btn.background_color = 0, 0, 0, .5

    def delete(self):
        try:
            os.remove(self.config_data.get('Record', 'PathSetting'))
            self.rec_btn.text = "Record"

        except IOError:
            pass
        # self.del_Btn.color = 1, 1, 1, 0.2
        # self.del_Btn.background_color = 0, 0, 0, 0.2

    def exit(self):
        App.get_running_app().stop()
        Window.close()

    def send(self):
        p_send = Process(target=Upload, args=(self.config_data,))
        p_send.start()

    def delete_pickle(self):
        try:
            os.remove('token.pickle')

        except IOError:
            pass


class WaveReco(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):

        self.settings_cls = SettingsWithTabbedPanel
        self.use_kivy_settings = False
        sm = ScreenManager()
        sm.add_widget(MainWindow(self.config))
        return sm

    def build_config(self, config):

        config.setdefaults('Record', {
            'SamplingSetting': '40000',
            'PlaybackSetting': False,
            'DurationSetting': '5',
            'ChannelSetting': '2',
            'ExtensionSetting': '.wav',
            'File_Name': 'Recording',
            'PathSetting': Common_path
        })
        config.setdefaults(
            'Upload', {
                'AccessSetting': 'reader',
                'FileTarget': 'Test_file',
                'User_Email': 'user@gmail.com',
            })

    def build_settings(self, settings):

        settings.add_json_panel('Audio',
                                self.config,
                                data=Recording_settings_json)

        settings.add_json_panel('Cloud',
                                self.config,
                                data=Upload_settings_json)

    def on_config_change(self, config, section, key, value):
        #  print(config, section, key, value)
        if key == "SamplingSetting":
            if int(value) > 384000:
                self.config.set("Record", "SamplingSetting", 384000)
                self.config.write()
                self.destroy_settings()
            elif int(value) < 1000:
                self.config.set("Record", "SamplingSetting", 1000)
                self.config.write()
                self.destroy_settings()

        sampling = int(config.get("Record", "SamplingSetting"))
        duration = int(config.get("Record", "DurationSetting"))
        channels = int(config.get("Record", "ChannelSetting"))  # number of channels
        max_memory = 190000000  # size of max matrix
        if key == "DurationSetting":
            if int(value) * sampling * channels > max_memory:
                self.config.set("Record", "DurationSetting", round(max_memory / (sampling * channels)))
                self.config.write()
                self.destroy_settings()

        elif key == "SamplingSetting":
            if int(value) * duration * channels > max_memory:
                self.config.set("Record", "SamplingSetting",
                                384000 if round(max_memory / (duration * channels)) >= 384000 else round(
                                    max_memory / (duration * channels)))
                self.config.write()
                self.destroy_settings()

        elif key == "ChannelSetting":
            if int(value) * duration * sampling > max_memory:
                self.config.set("Record", "ChannelSetting", 1)
                self.config.write()
                self.destroy_settings()

    def display_settings(self, settings):  # customization of settings
        try:
            p = self.settings_popup
        except AttributeError:
            self.settings_popup = Popup(content=settings,
                                        title='Settings',
                                        size_hint=(0.9, 0.9))
            p = self.settings_popup
        if p.content is not settings:
            p.content = settings
        p.open()

    def close_settings(self, settings, *args):
        try:
            p = self.settings_popup
            p.dismiss()
        except AttributeError:
            pass  # Settings popup doesn't exist


class Upload:
    def __init__(self, config_data):
        self.CLIENT_SECRET_FILE = 'wavereco_test_pc.json'  # ! remember to change !
        self.API_NAME = 'drive'
        self.API_VERSION = 'v3'
        self.SCOPES = ['https://www.googleapis.com/auth/drive']  # full scope
        self.config_data = config_data
        # creating service
        self.service = self.authorization(self.CLIENT_SECRET_FILE, self.API_NAME, self.API_VERSION, self.SCOPES)

        # uploading file
        # if user_email and access = None uploaded file won't be shared
        try:
            file_to_send = os.path.join(self.config_data.get('Record', 'PathSetting'))
            self.upload(folder_name=self.config_data.get('Upload', 'FileTarget'),
                        # file_name=self.config_data.get('Record', 'File_Name')+self.config_data.get('Record', 'ExtensionSetting'),
                        file_name=file_to_send,  ### file name = path
                        user_email=self.config_data.get('Upload', 'User_Email'),
                        access="" if self.config_data.get('Upload',
                                                          'AccessSetting') == "None" else self.config_data.get('Upload',
                                                                                                               'AccessSetting'))

        except IOError:
            pass

    def authorization(self, client_secret_file, api_name, api_version, scope):
        creds = None
        Window.close()

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

    def upload(self, folder_name, file_name, user_email=None, access=None):
        mime = 'application/vnd.google-apps.folder'  # MIME type - identifies file format
        folder_identifier = None
        page_token = None

        # CHECKS IF FOLDER ALREADY EXISTS
        response = self.service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                             spaces='drive',
                                             fields='nextPageToken, files(id, name)',
                                             pageToken=page_token).execute()
        for file in response.get('files', []):
            if file.get('name') == folder_name:
                folder_identifier = file.get('id')
                # gets permissions on the file
                perm = self.service.permissions().list(fileId=folder_identifier,
                                                       fields='permissions(emailAddress, role)').execute()
                # deletes owner email from permissions list
                shared_users = [i for i in perm['permissions'] if not (i['role'] == 'owner')]
                # print(shared_users)
                break

        # IF NO FOLDER CREATED
        if not folder_identifier:
            # creating folder
            folder_metadata = {  # resources are represented by metadata
                'name': folder_name,
                'mimeType': mime
            }
            folder = self.service.files().create(body=folder_metadata, fields='id').execute()  # creates folder
            folder_identifier = folder.get('id')  # gets folder id for creating permission
            # shares folder
            if user_email and access:
                permission_body = {
                    "kind": "drive#permission", "type": "user",
                    "emailAddress": user_email, "role": access
                }
                self.service.permissions().create(fileId=folder_identifier, body=permission_body).execute()
        # IF FOLDER CREATED
        else:
            # IF NOT SHARED WITH ANYONE
            if not shared_users:
                # IF WE WANT TO SHARE WITH SOMEONE
                if user_email and access:
                    permission_body = {
                        "kind": "drive#permission", "type": "user",
                        "emailAddress": user_email, "role": access
                    }
                    self.service.permissions().create(fileId=folder_identifier, body=permission_body).execute()
                # IF NO, WE MOVE ON
                else:
                    pass
            # IF SHARED WITH SOMEONE
            else:
                for user in shared_users:
                    # IF WE HAVE GIVEN SAME EMAIL AGAIN
                    if user['emailAddress'] == user_email and user['role'] == access:
                        pass
                    # IF WE HAVE GIVEN SAME EMAIL BUT OTHER ROLE ('reader' , 'writer')
                    # WE ARE CREATING NEW FOLDER WITH SIMILAR NAME
                    elif user['emailAddress'] == user_email and user['role'] != access:
                        suffix = str(datetime.datetime.now())
                        folder_metadata = {
                            'name': folder_name + " " + suffix[:-7],
                            'mimeType': mime
                        }
                        folder = self.service.files().create(body=folder_metadata, fields='id').execute()
                        folder_identifier = folder.get('id')  # gets folder id for creating permission
                        permission_body = {
                            "kind": "drive#permission", "type": "user",
                            "emailAddress": user_email, "role": access
                        }
                        self.service.permissions().create(fileId=folder_identifier, body=permission_body).execute()
                    # IF WE WANT TO SHARE FOLDER WITH NEXT PERSON
                    else:
                        permission_body = {
                            "kind": "drive#permission", "type": "user",
                            "emailAddress": user_email, "role": access
                        }
                        self.service.permissions().create(fileId=folder_identifier, body=permission_body).execute()

        # UPLOAD
        file_metadata = {
            'name': file_name,
            'parents': [folder_identifier]  # ID of parent folder
        }

        # selecting MIME type
        if file_name[-4:] == ".wav":
            file_mime = 'audio / wav'
        elif file_name[-4:] == ".mp3":
            file_mime = 'audio / mpeg'
        elif file_name[-5:] == ".flac":
            file_mime = "audio / flac"

        # creating MediaFileUpload object
        media = MediaFileUpload(file_name, mimetype=file_mime)
        self.service.files().create(  # creates file based on file and media metadata
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        return None


if __name__ == '__main__':
    WaveReco().run()
    freeze_support()
