import pyrebase
from pymongo import MongoClient
from querys import Querys

consultas = Querys("mongodb://localhost:27017")

firebase_config = {
    'apiKey': "AIzaSyDLrHdm-JQGx7q6t2b6AvDF93LQ-IFY4I8",
    'authDomain': "bottrade2-32afa.firebaseapp.com",
    'projectId': "bottrade2-32afa",
    'storageBucket': "bottrade2-32afa.appspot.com",
    'messagingSenderId': "174910244233",
    'appId': "1:174910244233:web:898c9297c2ad44777bcd58",
    'measurementId': "G-ZLKH7WQGHZ",
    'databaseURL': ''
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth() 

def login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        lista = consultas.obtenerDatosUsuario(user['localId'])
        print("Inicio de sesión exitoso. ID de usuario:", user['localId'])
        return lista
    except auth.EmailNotFoundException:
        print("Usuario no encontrado.")
        return {}
    except auth.WrongPasswordException:
        print("Contraseña incorrecta.")
        return {}
    except Exception as e:
        print("Error al iniciar sesión:", str(e))
        return {}

def registro(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        print("Registro exitoso. ID de usuario:", user['localId'])
        consultas.registrarId(user['localId'])
        return str(user['localId'])
    except Exception as e:
        print("Error al registrar usuario:", str(e))
        return {}





    