from pymongo import MongoClient
from django.conf import settings

def get_db():
    # Se agregan opciones para evitar problemas de certificados SSL comunes en Windows
    # y reducir el timeout para que no se cuelgue tanto tiempo si falla.
    client = MongoClient(
        settings.MONGO_URI, 
        tlsAllowInvalidCertificates=True,
        serverSelectionTimeoutMS=5000
    )
    return client['CatequesisDB']
