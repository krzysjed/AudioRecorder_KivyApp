import pickle
import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def authorization(client_secret_file, api_name, api_version, scope):

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


def upload(folder_name, file_name, user_email=None, access=None):

    # creating folder
    mime = 'application/vnd.google-apps.folder'  # MIME type - identifies file format
    folder_metadata = {                         # resources are represented by metadata
        'name': folder_name,
        'mimeType': mime
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()  # creates folder
    folder_identifier = folder.get('id')  # gets folder id for creating permission

    # adding permission to folder and it's content if...
    if user_email and access:
        permission_body = {
            "kind": "drive#permission",
            "type": "user",
            "emailAddress": user_email,
            "role": access
        }
        service.permissions().create(fileId=folder_identifier, body=permission_body).execute()

    # selecting MIME type
    if file_name[-4:] == ".wav":
        file_mime = 'audio / wav'
    elif file_name[-4:] == ".mp3":
        file_mime = 'audio / mpeg'
    elif file_name[-5:] == ".flac":
        file_mime = "audio / flac"
    
    # uploading file
    file_metadata = {  # resources are represented by metadata
        'name': file_name,
        'parents': [folder_identifier]  # ID of parent folder
    }

    # creating MediaFileUpload object
    media = MediaFileUpload(file_name, mimetype=file_mime)
    service.files().create(  # creates file based on file and media metadata
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    return None


if __name__ == '__main__':

    CLIENT_SECRET_FILE = 'wavereco_test_pc.json'        # ! remember to change !
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']  # full scope

    # creating service
    service = authorization(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    # uploading file
    # if user_email and access = None uploaded file won't be shared
    upload(folder_name="test_folder", file_name="epicsaxguy.wav",
           user_email="mikolaj.telec@gmail.com", access="reader")
           

    print("end")
