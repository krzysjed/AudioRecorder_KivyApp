## _Google Drive API_

This **REST API** allows us to integrate our app with Google Drive cloud storage. Thanks to it every user will be able to  
upload audio file to his **My Drive**.  API uses OAuth 2.0 authorization protocol which authenticates user before every data flow.    

### OAuth 2.0 authorization protocol

To get access to the API, every app must be registered on **Google APIs** site. Then Google provides developer with  
**credentials.json**, which contains **Client ID** and a **client secret**. Those strings are unique for every application.  
Thanks to those, app user will **acquire access** and **refresh tokens**. For safety reasons credentials should be   
kept in safe place, away from unauthorized users.

When app needs access to user private data, first it asks Google for specific **scope of access** using credentials  
gained before. Scopes define app access level to the user cloud storage (set of operations). After that, user is asked     
to authorize app action on his Google account. Then, Google grants application tokens mentioned earlier.   
Access token have short live time, but refresh tokens do not, so app will be able to acquire new access tokens,   
when previous one will expire. Finally, application can request user data.  


----

** not finished **



