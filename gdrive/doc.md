## _Google Drive API_

This **REST API** allows us to integrate our app with Google Drive cloud storage. Thanks to it every user will be able to  
upload audio file to his **My Drive** or maybe even **Shared Drive**.  API uses OAuth 2.0 authorization protocol which   
authenticates user before every data flow.  

----

To get access to the API, every app must be registered on **Google APIs** site. Then Google provides developer with  
**credentials.json**, which contains client ID and a client secret.  Thanks to this, application will have access to   
user data in cloud storage. 

When app needs access to user data, it sends request to Google with specific **scope of access**.  
Scopes define user access level to the cloud storage (what user can do etc.). After sending request,  
user is asked to authorize app action on his Google account. Then, Google grants application  
a access token (**token.pickle**) and data flow can be started.

----



