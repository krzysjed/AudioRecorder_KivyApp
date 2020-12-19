## _Google Drive API_

This **REST API** allows us to integrate our app with Google Drive cloud storage. Thanks to it every user will be able to  
upload audio file to his **My Drive**.  API uses OAuth 2.0 authorization protocol which   
authenticates user before every data flow.  

### OAuth 2.0 authorization protocol

To get access to the API, every app must be registered on **Google APIs** site. Then Google provides developer with  
**credentials.json**, which contains client ID and a client secret.  Thanks to those, every app user will be granted  
access and refresh tokens.

When app needs access to user data, first it asks Google for specific **scope of access**.    
Scopes define user access level to the cloud storage (what user can do etc.). After that,      
user is asked to authorize app action on his Google account. Then, Google grants application    
tokens mentioned earlier. Access token expire, but refresh tokens do not, so app will be able   
to acquire new access token. Finally, application can request user data.


----

** not finished **



