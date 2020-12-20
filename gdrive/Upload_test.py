"""
Script tests uploading file to new directory
-----------------------------------------------------------------------------------------------
Imports:
    pickle
        - used for pickling and unpickling tokens.
        - 'pickling' - Python object converted into a byte stream
        - 'unpickling' - inverse operation of pickling
    os.path
        - simple pathname manipulations
    time
        - used for measuring execution time
    googleapiclient.discovery
        - provides build(serviceName, version, credentials) function which constructs Resource
        for interaction with API,
    googleapiclient.http
        - provides MediaFileUpload class
    google_auth_oauthlib.flow
        - provides InstalledAppFlow class used for acquiring tokens
    google.auth.transport.requests
        - provides Request class, Credentials class
----------------------------------------------------------------------------------------------
Functions:
    authorization():
        - generates access tokens based on provided credentials.json and saves them into a token.pickle file,
        - checks if token is valid. If not, token is refreshed.
        - constructs Resource object for interaction with API
    -----------------------------------------------------------
    create_folder():
        - creates folder in user My Drive with specified name
        - returns created folder ID
    -----------------------------------------------------------
    upload_file():
        - uploads file to a specified folder
"""

import pickle
import os.path
import time
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']  # full scope


def authorization(client_secret_file, api_name, api_version, scope):
    """
    OAuth2 app authorization
    Parameters
    ----------
    client_secret_file: str
            Name of credentials.json file
    api_name: str
            Name of API e.g. 'drive'
    api_version: str
            Version of API
    scope: [str]
            Scope of access

    Returns
    -------
    drive_service: Resource object
        Resource with methods for interaction with API
    """

    creds = None

    # if token already exists
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # if no tokens or token is expired
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Credential refreshed !!!")
            creds.refresh(Request())  # token refreshing
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scope)  # token generation
            creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)  # saving access token in token.pickle

    drive_service = build(api_name, api_version, credentials=creds)  # constructs Resource for interaction with API
    print("Authorization complete!")
    return drive_service


def create_folder(name):
    """
    Creates folder in user My Drive
    Parameters
    ----------
    name: str
          Folder name

    Returns
    -------
    identifier: str
          Folder ID sequence
    """
    mime = 'application/vnd.google-apps.folder'     # MIME type - identifies file format
    identifier = None       # holds Folder ID (last sequence in URL address, when folder is opened)

    folder_metadata = {         # resources are represented by metadata
        'name': name,
        'mimeType': mime
    }
    service.files().create(body=folder_metadata).execute()  # creates folder specified in metadata

    # looking for ID of created folder
    response = service.files().list(spaces='drive',     # searches only in My Drive
                                    fields='nextPageToken, files(name, id)',    # what should be included in response
                                    ).execute()
    items = response.get('files', [])   # saves response in list
    for item in items:
        if item['name'] == name:            # looking for folder ID
            identifier = item['id']
            break

    print("Folder created!")
    return identifier


def upload_file(file_name, file_mime, dir_id):
    """
    Uploads file to specified folder
    Parameters
    ----------
    file_name: str
        File name
    file_mime: str
        Defines file type
    dir_id: str
        Folder ID sequence
    Returns
    -------
        None
    """
    file_metadata = {       # resources are represented by metadata
        'name': file_name,
        'parents': [dir_id]     # ID of parent folder
    }

    media = MediaFileUpload(file_name, mimetype=file_mime)  # creates MediaFileUpload class object
    service.files().create(     # creates file based on file and media metadata
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    print('Upload finished!')


if __name__ == '__main__':
    start_time = time.time()
    service = authorization(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)  # returns Resource object
    folder_id = create_folder('test_folder')  # creates folder
    up_start = time.time()
    upload_file('file_example_WAV_10MG.wav', 'audio / wav', folder_id)  # uploads file
    end_time = time.time()
    upload_time = end_time - up_start
    execution_time = end_time - start_time

    print(f"It took {execution_time} seconds to execute program.\n",
          f"It took {upload_time} seconds to upload file")
