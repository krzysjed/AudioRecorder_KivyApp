import json

settings_json = json.dumps([

    {'type': 'options',
     'title': 'Numbers of Channels',
     'desc': 'Numbers of Channels 1-2',
     'section': 'example',
     'key': 'ChannelSetting',
     'options': ['1', '2']},

     {'type': 'options',
      'title': 'Extension',
      'desc': 'Extension',
      'section': 'example',
      'key': 'ExtensionSetting',
      'options': ['.wav', '.mp3','.flac']},

    {'type': 'string',
     'title': 'A string setting',
     'desc': 'String description text',
     'section': 'example',
     'key': 'stringexample'},
    {'type': 'path',
     'title': 'A path setting',
     'desc': 'Path description text',
     'section': 'example',
     'key': 'pathexample'}])

