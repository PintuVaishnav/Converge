import pyrebase

def init_firebase():
    config = {
        "apiKey": "AIzaSyCDdqVDPaCP0lnfOyh3FzZ4Vcdov_5kQvE",
        "authDomain": "converge-chatapp.firebaseapp.com",
        "projectId": "converge-chatapp",
        "storageBucket": "converge-chatapp.appspot.com",
        "messagingSenderId": "926570624998",
        "appId": "1:926570624998:web:dfe8ff1850be8fcc68c827",
        "measurementId": "G-31CXS61FBL",
        "databaseURL": "https://converge-chatapp-default-rtdb.firebaseio.com/"
    }
    firebase = pyrebase.initialize_app(config)
    return firebase





