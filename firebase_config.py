import pyrebase

def init_firebase():
    config = {
        "apiKey": "your-api-key",
        "authDomain": "your-auth-domain.firebaseapp.com",
        "projectId": "your-project-id",
        "storageBucket": "your-storage-bucket.appspot.com",
        "messagingSenderId": "your-messaging-sender-id",
        "appId": "your-app-id",
        "measurementId": "your-measurement-id",
        "databaseURL": "https://your-database-url.firebaseio.com/"
    }
    return pyrebase.initialize_app(config)
