## _Google Drive API_

This **REST API** allows us to integrate our app with Google Drive cloud storage. Thanks to it every user will be able to  
upload audio file to his **My Drive**.  API uses OAuth 2.0 authorization protocol which authenticates user before every data flow.    

----
### OAuth 2.0 authorization protocol

To get access to the API, every app must be registered on **Google APIs** site. Then Google provides developer with  
**credentials.json**, which contains **Client ID** and a **client secret**. Those strings are unique for every application.  
Thanks to those, app user will **acquire access** and **refresh tokens**. For safety reasons credentials should be   
kept in safe place, away from unauthorized users.

When app needs access to user private data, first it asks Google for specific **scope of access** using credentials  
gained before (**.json file**). Scopes define app access level to the user cloud storage (set of allowable operations).   
After that, user is asked to authorize app action on his Google account. Then, Google grants application tokens mentioned earlier.   
Access token have short live time, but refresh tokens do not, so app will be able to acquire new access tokens,   
when previous one will expire. 

After completing those steps, application can start data flow.

----
### Libraries

Below is list of libraries used for handling Google Drive API:  
- **googleapiclient** - core library for every Google API,
- **google.auth** - Google authentication library for Python,
- **google_auth_oauthlib** - library which contains oauthlib integration with google-auth. Makes authorization process simpler.  

List may change in the future.  

----
### Tests

For tests purpose two scripts were written. 
- **OAuth2_test.py** 
- **Upload_test.py**

Because of safety reasons, .json credential file which was used for tests is not provided.  
Scripts should work on every .json credentials.

###### OAuth2_test.py

Contains functions:
- **auth2_test()**, 

This Python script tests OAuth2 authorization protocol. It includes generation, validation and refreshing of access tokens.  
Uses scope, which allows only read of file metadata. Script returns 10 last used files names and id's on Google Drive by user.

###### Upload_test.py

Contains functions:  
- **authorization()**,
- **create_folder()**,
- **upload_file()**,

This Python script tests data upload to My Drive folder. For tests we have used 10 MB audio file in .wav format (nearly 1 minute long).  
Uploading took 13 seconds of execution time, which was nearly 16 seconds.

Audio .wav file is not included.

----

### Reference documentation
Useful links. Content on one site may be similiar to content on the other site.  
- [Introduction to Google Drive API](https://developers.google.com/drive/api/v3/about-sdk)
- [API reference](https://developers.google.com/drive/api/v3/reference)
- [Drive API instance methods](https://googleapis.github.io/google-api-python-client/docs/dyn/drive_v3.html)
- [googleapiclient core library docs](https://googleapis.github.io/google-api-python-client/docs/epy/index.html) - **hard to read** 
- [googleapiclient github site](https://github.com/googleapis/google-api-python-client)
- [google.auth](https://google-auth.readthedocs.io/en/latest/index.html)
- [google_auth_oauthlib](https://google-auth-oauthlib.readthedocs.io/en/latest/#)
