import firebase_admin
from firebase_admin import credentials, firestore

# OneHR Dev
cred_dev = credentials.Certificate("secrets/onehr-dev.json")
app_dev =firebase_admin.initialize_app(cred_dev, name="dev")
db_dev = firestore.client(app=app_dev)

# OneHR Internal
cred_internal = credentials.Certificate("secrets/onehr-internal.json")
app_internal = firebase_admin.initialize_app(cred_internal, name="internal")
db_internal = firestore.client(app=app_internal)


