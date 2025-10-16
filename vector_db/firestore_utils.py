def fetch_documents(db, collection_name):
    """Fetch all documents from a Firestore collection."""
    return [doc.to_dict() for doc in db.collection(collection_name).stream()]
