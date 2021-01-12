## Description

This directory contains everything about Google Drive API.

----

#### **Upload prototype** 

###### **Upload_proto.py**

Contains authorization function and upload function. 
Three types of audio files can be sent: .mp3, .wav, .flac.   
Also access can be given to the other users. Files are uploaded to a new folder with specified name.

#### **Tests**

###### **OAuth2_test.py**

Contains functions:
- **auth2_test()**, 

This Python script tests OAuth2 authorization protocol. It includes generation, validation and refreshing of access tokens.  
Uses scope, which allows only read of file metadata. Script returns 10 last used files names and id's on Google Drive by user.

###### **Upload_test.py**

Contains functions:  
- **authorization()**,
- **create_folder()**,
- **create_permission()**, 
- **upload_file()**,

This Python script tests data upload to My Drive folder. For tests we have used 10 MB audio file in .wav format (nearly 1 minute long).  
Uploading took 13 seconds of execution time, which was nearly 16 seconds.

Audio .wav file is not included.
