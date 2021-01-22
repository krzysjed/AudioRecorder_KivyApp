import json

Recording_settings_json = json.dumps([

    {'type': 'options',
     'title': 'Numbers of Channels',
     'desc': 'Numbers of Channels 1-2',
     'section': 'Record',
     'key': 'ChannelSetting',
     'options': ['1', '2']},

    {'type': 'numeric',
     'title': 'Duration',
     'desc': 'Audio recording time',
     'section': 'Record',
     'key': 'DurationSetting'},

    {'type': 'numeric',
     'title': 'Sampling',
     'desc': 'Sound recording frequency(1k-384k)',
     'section': 'Record',
     'key': 'SamplingSetting'},

    {'type': 'bool',
         'title': 'Modifying the playback frequency',
         'desc': 'OFF - default playback / ON - modify the playback frequency(set your value in the above sampling box',
         'section': 'Record',
         'key': 'PlaybackSetting'},

    {'type': 'options',
     'title': 'Extension',
     'desc': 'Extension',
     'section': 'Record',
     'key': 'ExtensionSetting',
     'options': ['.wav', '.mp3','.flac']},

    {'type': 'string',
     'title': 'File name',
     'desc': 'Record file name',
     'section': 'Record',
     'key': 'File_Name'},

    {'type': 'path',
     'title': 'A path of audio files',
     'desc': 'Select the audio file which you want to use',
     'section': 'Record',
     'key': 'PathSetting'}
   ])


Upload_settings_json = json.dumps([

     {'type': 'options',
      'title': 'Access',
      'desc': 'User level of access',
      'section': 'Upload',
      'key': 'AccessSetting',
      'options': ['reader', 'writer', 'None']},

     {'type': 'string',
      'title': 'Folder name',
      'desc': 'The name of the target folder in google disk',
      'section': 'Upload',
      'key': 'FileTarget'},

     {'type': 'string',
      'title': 'User_email',
      'desc': "Target person's mail",
      'section': 'Upload',
      'key': 'User_Email'}])

