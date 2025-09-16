import firebase_admin
from firebase_admin import credentials, firestore

# Path to your service account key
cred = credentials.Certificate("secrets/serviceAccountKey.json")

# Initialize Firebase
firebase_admin.initialize_app(cred)

# Connect to Firestore
db = firestore.client()

# Example: list all collections
collections = db.collections()
for col in collections:
    print("Collection:", col.id)

def explore_collection(collection_name, limit=5):
    """Prints first few documents and their fields in a collection"""
    print(f"\n--- Exploring collection: {collection_name} ---")
    docs = db.collection(collection_name).limit(limit).get()
    if not docs:
        print("No documents found.")
        return
    for doc in docs:
        print(f"Document ID: {doc.id}")
        print(f"Fields: {doc.to_dict()}\n")

# Example usage: explore the 'employee' collection
# explore_collection("employee", limit=5)
